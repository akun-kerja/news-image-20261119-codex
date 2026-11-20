import { copyFile, mkdir, stat } from "node:fs/promises";
import { join } from "node:path";

const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
await mkdir(outputDir, { recursive: true });
const sourcePath = new URL("./entry.png", import.meta.url);
const outputPath = join(outputDir, "entry.png");
await copyFile(sourcePath, outputPath);

const [source, output] = await Promise.all([stat(sourcePath), stat(outputPath)]);
if (!output.isFile() || output.size !== source.size) {
  throw new Error(`Copied image verification failed: ${outputPath}`);
}
console.log(`${outputPath} ${output.size} bytes`);
