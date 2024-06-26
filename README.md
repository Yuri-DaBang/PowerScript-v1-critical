## PowerScript 🚀

A programming language inspired by many things, aiming to attract all kinds of developers! 😎 Well, okay, maybe not everyone, but we've got a pretty good shot!

## Features
- User can add custom commands and things to the language easily.
- Pre-added builtin libs like `math`,`physics`,`matplotlib`,`console` and many more.
- A supercool [PackageManager](src\SideAutomations\pm.py) like `npm`, but better then `npm` but it cannot install packages from web, LOL😅 .

## Known errors
- The import command dosent work fine 😅.

### Getting Started

Let's dive right into our programming language with the ever-popular FizzBuzz challenge:

```zig
/**
 * A fun little challenge to categorize numbers into three groups...
 */

let rng_start (
  readln!("Enter the starting point of the range: ")
  .toint()
);
let rng_end (
  readln!("And also the end: ")
  .toint()
);
if rng_start >= rng_end {
  println("The start value must be smaller than the end value!");
  exit!(1);
}

for let i in [rng_start..rng_end] {
  if ((% i 15) == 0) {
    println("...Fizzbuzz");
  } else if ((% i 3) == 0) {
    println("...Fizz");
  } else if ((% i 5) == 0) {
    println("...Buzz");
  } else {
    println("${i}"); // Or just pass `i` as an argument!
  }
}
```

Yes, we use **prefix notation for mathematical operations** that clearly indicate priorities. In some cases you should also put an **equal sign behind the open brace before starting a block**...

Would you like to see more code samples from the Infiniti3 programming language? Go to the [examples](examples) folder...

## Usage

To run a `.infy` file, use the `run` command:

```bash
Infiniti3 run examples/linear_search/sol02.infy
```

Remember to replace the example code with your own Infiniti3 code.

To start an interactive Infiniti3 shell (REPL), use the `shell` command:

```bash
Infiniti3 shell
```

To swiftly execute Infiniti3 code snippets right from your command line, use the `cmd` command:

```bash
Infiniti3 cmd 'println("Hello, world!");'
```

This project is licensed under the MIT license found in the [LICENSE](LICENSE) file in the root directory of this repository.

### Disclaimer

As you know, you shouldn't use this language for a serious product [at least not yet]! 😅
