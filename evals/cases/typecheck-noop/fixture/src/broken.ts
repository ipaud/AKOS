// A type error that the root `tsc --noEmit` will never see, because the root
// tsconfig is a solution file: `files: []` means it validates zero files and
// exits 0 regardless of what is in src/.
export const count: number = "not a number";
