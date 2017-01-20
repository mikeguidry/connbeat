import os
import stat
import connbeat
from nose.plugins.attrib import attr

class ConnectionTest(connbeat.BaseTest):
    @attr('integration')
    def test_connection(self):
        """
        Basic connections are published
        """
        self.render_config_template()
        os.environ['PROC_NET_TCP'] = '../../tests/files/proc-net-tcp-test-small'

        proc = self.start_beat()
        self.wait_until(lambda: self.output_lines() > 0)
        proc.check_kill_and_wait()

        output = self.read_output_json()
        evt = output[0]

        self.assertEqual(evt['local_port'], 80)

        evt = output[1]
        self.assertEqual(evt['local_port'], 631)

        evt = output[2]
        self.assertEqual(evt['local_port'], 40074)
        self.assertItemsEqual(evt['beat']['local_ips'], ['192.168.2.243'])
