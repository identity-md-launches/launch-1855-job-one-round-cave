#!/usr/bin/env python3
"""Run Endpoint Sentry under a separate-process wall-clock watchdog."""
import argparse
import json
import math
from pathlib import Path
import subprocess
import sys
import time


def supervise(command, deadline):
    """Internal process supervisor; command is constructed locally by main.

    communicate's timeout covers DNS, TLS, header and body stalls in the child.
    A timed-out child is killed and reaped, without retrying the GET.
    """
    started = time.monotonic()
    try:
        child = subprocess.Popen(command, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError as error:
        return {'ok': False, 'error': {'kind': 'worker_start', 'message': str(error)}}, 1
    try:
        remaining = max(0, deadline - (time.monotonic() - started))
        stdout, stderr = child.communicate(timeout=remaining)
    except subprocess.TimeoutExpired:
        child.kill()
        child.communicate()
        return {'ok': False, 'error': {
            'kind': 'deadline',
            'message': 'Worker exceeded wall-clock budget and was killed; no retry was made.'},
            'worker_returncode': child.returncode,
            'partial_report_discarded': True}, 1
    if child.returncode == 2:
        return {'ok': False, 'error': {'kind': 'arguments',
                                     'message': stderr.decode('utf-8', 'replace').strip()}}, 2
    try:
        report = json.loads(stdout)
        if not isinstance(report, dict) or type(report.get('ok')) is not bool:
            raise ValueError('worker report missing boolean ok')
        if child.returncode not in (0, 1) or (child.returncode == 0) != report['ok']:
            raise ValueError('worker exit status contradicts report')
    except (ValueError, UnicodeError) as error:
        return {'ok': False, 'error': {'kind': 'worker_protocol', 'message': str(error)},
                'worker_returncode': child.returncode}, 1
    return {'ok': report['ok'], 'probe': report}, child.returncode


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False,
        epilog='All remaining arguments go to the unchanged Endpoint Sentry CLI. '
               'Example: --deadline 5 https://api.imd.fun/launches --json')
    parser.add_argument('--deadline', type=float, default=12,
                        help='parent wall-clock budget, 0 < seconds <= 120 (default 12)')
    args, sentry_args = parser.parse_known_args(argv)
    if not math.isfinite(args.deadline) or not 0 < args.deadline <= 120:
        parser.error('deadline must be finite, greater than zero and at most 120 seconds')
    if not sentry_args:
        parser.error('provide an HTTPS URL and optional Endpoint Sentry arguments')
    sentry = Path(__file__).resolve().parent.parent / 'endpoint-sentry' / 'sentry.py'
    # -I avoids ambient Python search paths; -B prevents bytecode writes.
    command = [sys.executable, '-I', '-B', str(sentry)] + sentry_args
    started = time.monotonic()
    result, code = supervise(command, args.deadline)
    result.update(schema='deadline-sentry/v1', deadline_seconds=args.deadline,
                  elapsed_ms=round((time.monotonic() - started) * 1000, 3))
    print(json.dumps(result, indent=2, allow_nan=False))
    return code


if __name__ == '__main__':
    sys.exit(main())
