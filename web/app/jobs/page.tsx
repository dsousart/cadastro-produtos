import { Wave2Dashboard } from "../../components/wave2-dashboard";
import { getHealthSample } from "../../lib/health";

export default async function JobsPage() {
  const health = await getHealthSample();
  return <Wave2Dashboard health={health} activeTab="jobs" />;
}
