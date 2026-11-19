import { createHash } from "node:crypto";
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  console.error("MAKEFUN_OUTPUT_DIR is not set");
  process.exit(1);
}

if (!existsSync(source)) {
  console.error(`entry.png not found at ${source}`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(source, dest);

const srcBytes = readFileSync(source);
const srcHash = createHash("sha256").update(srcBytes).digest("hex");

// The entry must be a whole PNG within the competition limits.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!srcBytes.subarray(0, 8).equals(PNG_MAGIC)) {
  console.error("entry.png is not a PNG (bad magic bytes)");
  process.exit(1);
}
if (srcBytes.length > 1048576) {
  console.error(`entry.png is ${srcBytes.length} bytes, over the 1 MiB limit`);
  process.exit(1);
}

const dstBytes = readFileSync(dest);
const dstHash = createHash("sha256").update(dstBytes).digest("hex");
if (srcHash !== dstHash) {
  console.error(`digest mismatch: source ${srcHash} != written ${dstHash}`);
  process.exit(1);
}

console.log(`wrote ${dest} sha256=${dstHash}`);
