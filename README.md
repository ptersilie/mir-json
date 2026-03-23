# MIR to JSON

Generate Rust MIR and store it as JSON. Maps function names to their respective
MIR body.

## Usage

Execute `sh run.sh`. This will:
- checkout a sample Rust project `sparsevec`
- dump the MIR at different optimisation levels: none, selected, full
- for each opt level create a JSON file at two MIR optimisation stages (before
  passes and after all passes)

The json files can then be found in:
- sparsevec/noopt_mir/{built,runtime-optimized}.json
- sparsevec/opt_mir/{built,runtime-optimized}.json
- sparsevec/PASSNAME_mir/{built,runtime-optimized}.json

## Some considerations

Not all optimisation passes can be disabled in Rust as quite a few are required
by the pipeline. The minimum amount of passes can be achieved with

```
cargo +nightly rustc -- -C opt-level=0 -Z mir-opt-level=0 -Zdump-mir=all
```

This still leaves many passes enabled. The command dumps MIR files after each
optimisation pass, so we have some control over which stage of the pipeline we
care about most. For now, I have opted to generate JSON files at two stages of
the pipeline (though this can easily be adjusted in the Python script):

- `built`: no passes have run
- `runtime-optimized`: all passes have run

Examples of other options we could collect here and might be interesting are:
`SimplifyCfg-post-analysis`, `ForceInline`, `PromoteTemps`

## Disabling/enabling passes

Even though many of the optimisation passes are required, there are some that
can be toggled via `-Z mir-enable-passes=+Passname`. In `run.sh` we are thus
also selectively applying a handful of passes to the minumum build. This can be
extended with other passes we may care about, with examples of other options
being:

- LowerSliceLenCalls
- InstSimplify-before-inline
- RemoveStorageMarkers
- RemoveZsts
- RemoveUnneededDrops
- UnreachableEnumBranching
- SimplifyCfg-after-unreachable-enum-branching
- InstSimplify-after-simplifycfg
- SimplifyConstCondition-after-inst-simplify
- SimplifyLocals-before-const-prop
- SimplifyLocals-after-value-numbering
- MatchBranchSimplification
- SingleUseConsts
- RemoveNoopLandingPads
- CopyProp
- AddCallGuards
- PreCodegen
