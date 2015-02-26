import xmostest
import os
from xmostest.xmostest_subprocess import call
from uart_rx_checker import UARTRxChecker, Parity


def do_test(baud):
    myenv = {'baud': baud, 'parity': 'UART_PARITY_EVEN'}
    path = "app_uart_test_rx"
    resources = xmostest.request_resource("xsim")

    checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", Parity['UART_PARITY_BAD'], baud, 4, 1, 8)
    tester = xmostest.ComparisonTester(open('test_rx_bad_uart.expect'),
                                       "lib_uart", "sim_regression", "rx_bad", myenv,
                                       regexp=True)

    # Only want no parity @ 230400 baud for smoke tests
    if baud != 115200:
        tester.set_min_testlevel('nightly')
    if not tester.test_required():
        return

    xmostest.build(path, env=myenv, do_clean=True)

    xmostest.run_on_simulator(resources['xsim'],
                              'app_uart_test_rx/bin/smoke/app_uart_test_rx_smoke.xe',
                              simthreads=[checker],
                              xscope_io=True,
                              tester=tester,
                              simargs=["--vcd-tracing", "-tile tile[0] -ports -o trace.vcd"])


def runtests():
    for baud in [57600, 115200]:
        do_test(baud)