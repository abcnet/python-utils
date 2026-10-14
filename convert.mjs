import GLSL from "glsl-transpiler";
import { readFileSync, writeFileSync } from "node:fs";

const input = process.argv[2] ?? "-";
const output = process.argv[3] ?? "-";

const source = input === "-"
    ? readFileSync(0, "utf8")
    : readFileSync(input, "utf8");

const compile = GLSL();
const result = compile(source);

if (output === "-") {
    process.stdout.write(result);
} else {
    writeFileSync(output, result);
}