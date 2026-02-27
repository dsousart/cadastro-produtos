import { spawnSync } from "node:child_process";

const steps = [
  ["run", "lint"],
  ["run", "typecheck"],
  ["run", "test:unit"],
  ["run", "test"],
];

for (const args of steps) {
  const label = `npm ${args.join(" ")}`;
  console.log(`\n[release-gate] ${label}`);

  const result = spawnSync("npm", args, {
    stdio: "inherit",
    env: process.env,
    shell: true,
  });

  if (result.error) {
    console.error(`[release-gate] spawn error at: ${label}`, result.error.message);
    process.exit(1);
  }

  if (result.status !== 0) {
    console.error(`[release-gate] failed at: ${label}`);
    process.exit(result.status ?? 1);
  }
}

console.log("\n[release-gate] all checks passed");
