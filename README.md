### [Under Construction: 12/2/2022]

TODO: How to have multiple subparsers invoked at the same time?

Dev areas:
- [ ] registration hooks
- [ ] user definition
- [ ] resolution engine
- [ ] resolution api
- [ ] support list parameters

# Example Usage

DI usage consists of 3 phases:
1. Registration of objects through decorator hooks
2. Defining resolver parameters through a front-end (e.g., argparse)
3. Resolving objects

See the `examples` directory for full code examples.

## Front-Ends
### Arg-parse
Two use cases:
1. You want to use the parameters of some class in argparse.
    * Simply decorate your class and register the argparse frontend. The class will appear under its own command line option and be usable through `parser.parse_args()`.
2. You want to use argparse parameters to create the object container for later runtime resolution.
* Register a class as in step one. Use the container resolver to create an object at runtime from these parameters.

### Config File

# Testing
From the root project directory, run the Makefile: `make run_tests`