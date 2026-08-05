import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repositoryRoot = path.resolve(
    path.dirname(fileURLToPath(import.meta.url)),
    "..",
);
const checkerPath = path.join(
    repositoryRoot,
    ".pathnote",
    "pathnote-source-check.mjs",
);

if (!existsSync(checkerPath)) {
    console.error(
        "缺少 .pathnote/pathnote-source-check.mjs。请先安装同路志统一发布检查器。",
    );
    process.exit(1);
}

const requestedArguments = process.argv.slice(2);
const modeArguments =
    requestedArguments.length > 0 ? requestedArguments : ["--staged"];
const result = spawnSync(
    process.execPath,
    [checkerPath, "--source", "programming-lab", ...modeArguments],
    {
        cwd: repositoryRoot,
        stdio: "inherit",
    },
);

if (result.error) {
    console.error(result.error.message);
    process.exit(1);
}

if (result.signal) {
    console.error(`同路志内容检查被信号 ${result.signal} 终止。`);
    process.exit(1);
}

process.exit(result.status ?? 1);
