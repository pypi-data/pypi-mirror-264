import proto.dtx.messages.common.threat_pb2 as dtx_threat_pb2

from detoxio.reporting import LLMScanReport
from detoxio.models import LLMScanResult

def dtx_get_threat_name(tid):
    return dtx_threat_pb2.ThreatCategory.DESCRIPTOR.values_by_number[tid].name

def dtx_get_threat_class_name(tid):
    return dtx_threat_pb2.ThreatClass.DESCRIPTOR.values_by_number[tid].name

threat_classes = [value.name for value in dtx_threat_pb2.ThreatClass.DESCRIPTOR.values]
threat_categories = [value.name for value in dtx_threat_pb2.ThreatCategory.DESCRIPTOR.values]

class ConsoleReporter(LLMScanReport):
    def render(self, results: LLMScanResult):
        metrics = {
            'prompt_count': len(results.results),
            'vulnerabilities': {}
        }

        for r in results:
            for response in r.responses:
                for result in response.results:
                    threat_class = dtx_get_threat_class_name(result.threat.threat_class)
                    threat_name = dtx_get_threat_name(result.threat.threat_category)

                    metrics['vulnerabilities'][threat_class] = metrics['vulnerabilities'].get(threat_class, {})
                    metrics['vulnerabilities'][threat_class][threat_name] = metrics['vulnerabilities'][threat_class].get(threat_name, 0)

                    if result.status == dtx_threat_pb2.THREAT_EVALUATION_STATUS_UNSAFE:
                        metrics['vulnerabilities'][threat_class][threat_name] += 1

        # TODO: Enhance the rendering with a better visualization library
        for tk, tv in metrics['vulnerabilities'].items():
            for vk, vv in tv.items():
                print("{0:<20} {1:<20}: {2}".format(tk, vk, vv))

