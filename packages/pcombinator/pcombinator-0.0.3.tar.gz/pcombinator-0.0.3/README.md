![Build Status](https://github.com/RomansWorks/PCombinator/actions/workflows/build.yaml/badge.svg)
![Coverage Status](https://img.shields.io/codecov/c/github/RomansWorks/PCombinator)
![GitHub](https://img.shields.io/github/license/RomansWorks/PCombinator)
![PyPI version](https://img.shields.io/pypi/v/PCombinator)
![Python version](https://img.shields.io/badge/python-3.10-blue.svg)

# Some Relevant papers

1. [Premise Order Matters in Reasoning with Large Language Models](https://arxiv.org/pdf/2402.08939.pdf) . Note that this paper also measures how distractors affect the performance of the model.
2. [The Butterfly Effect of Altering Prompts: How Small Changes and Jailbreaks Affect Large Language Model Performance](https://arxiv.org/abs/2401.03729)
3. **Help needed** - additional references on the sensitivity of outcomes to minor variation in prompt (specifically find the separators article) 


# PCombinator

A handy tool for building, manipulating and evaluating **prompts** in both development and production. 

- 🎯 Generate variations of prompts for large language and vision models, and evaluate the effectiveness of each particle in the variation. With it you can systematically optimize your prompts. 
- 🎯 Combine prompts from hierarchical ingredients at runtime, for example when different invocations of a model require slightly different prompts, retrieval augmentation, and more.

Some examples of questions you can easily test using PCombinator:

- ✅ Is giving a an example (few shot) to the prompt contributes to effectiveness?
- ✅ Is a specific example or combination of examples better than the others?
- ✅ Is this additional instruction helpful?
- ✅ Is putting the examples before the rules or instructions better, or is it vice versa? (also see [article](https://arxiv.org/pdf/2402.08939.pdf))
- ✅ Which delimiter is the best for separating examples? (also see [])
- ✅ Does Chain of Though (CoT) help or just cost more?
- ✅ Does the order of the examples matter?
- ✅ Do I need this many examples?
- ✅ Should I use an instructive language or a more conversational one?
- ✅ Is a certain role for the model biases it better than another role?
- ✅ Which terms in a text2image prompt contribute more to the effectiveness of the prompt?
- ✅ Combine prompt injection techniques to evaluate how malicous users can exploit the model and overcome protections. (also see [article](https://arxiv.org/abs/2401.03729))

### Main Concepts

There are two parts to the library, each can be used independently:

1. The **Combinators** (arranged in a tree): which generate the prompts.
2. The **Evaluator**: which evaluates the effectiveness of the prompts. This is work in progress. 

#### Paths and Rendering

There are two main **actions** in the library:

1. **Generating** **Paths** - which are walks down the combinator tree, i.e. specific combinations of the ingredients in the tree. This is done using the `generate_paths` method of the combinator.
2. **Rendering** a prompt: The process of generating a prompt from a path in the combinator tree. This is done using the `render_path` method of the combinator.

Some metrics that can be used to evaluate the effectiveness of the prompts:
- 📈 The score given by a human or a model judge to the output. 
- 📈 Use score on existing labeled datasets and evaluators. 
- 📉 The perplexity of the model on the prompt. 

## How to use it?

A simple example is below. A more full example is in the `examples` folder and at the end of this document. 

### Installation

To install the full package, including the `templating` extension, use:

**Pip**: 

```bash
pip install pcombinator
# or with templating:
pip install pcombinator[templating]
```

**Poetry**:
  
```bash
poetry add pcombinator
# or with templating:
poetry add pcombinator --extras templating
```


### Simple example - LLMs

```python
import random
from pcombinator.combinators import JoinSomeOf, NamedString, Jinja2Template, PickOne


# Create the combinators
template_combinator = Jinja2Template(
    "{role}\n{instruction}.",
    children={
        "role": PickOne(
            id="role_combinator",
            children=[
                NamedString("variation_1", "You are a a useful assistant"),
                "As a helpful assistant",  # unnamed string
                None # If we want to try the prompt without the role
            ]
        ),
        "instruction": JoinSomeOf(
            id="instruction_combinator",
            n_min=1,
            n_max=2,
            children=[
                "Do A",
                "Perform A",
                "Execute A",
            ],
            separator=" or ",
        ),
    },
)

# Create all the possible paths in the tree
paths = template_combinator.generate_paths()

res = []
# Print out each created prompt and the path used to create it
for idx, path in enumerate(paths):

  # Render - this takes the path and creates the prompt
  rendered_prompt = root_combinator.render_path(path)

  # Save the prompt and the path for later evaluation
  res.append((rendered_prompt, path))

  # Print the prompt and the path
  print(rendered_prompt)
  print("-" * 80)
  print(path)
  print("=" * 80)


# Save the prompts and paths for later evaluation
with open("path/to/prompt.json", "w") as f:
    f.write(json.dumps(res))

```

See additional exampels in the `examples` folder and under `pcombinator/combinators/tests`.


### Simple Example - Vision Models

```python
# TODO
```


# Detailed explanation

## Currently available combinators

1. `JoinSomeOf`: Creates combinations of between n_min to n_max (inclusive) children in each combination. Renders with a separator between each child.
2. `NamedString`: A string with an identifier. Useful for tracking the contribution of each part of the prompt.
3. `PickOne`: Picks one of the children.
4. `Jinja2Template`: A Jinja2 template combinator. Fills the template with the children.

## How does it work?

PCombinator creates combinations of prompts from a tree of other combinators, and eventually string or None values at the leaves. It also stores the identifiers used to create the specific combination, for later evaluation of the effectiveness of each node in the tree. The evaluation functionality itself is not yet implemented.

# Path

The Path represents the specific identifiers used at each node in the tree to create a specific prompt. Essentially the "bill of materials".

With a Path object you can:
1. Render the prompt (using the `render_path` method of a combinator)
2. Associate the ingredients of the prompt with an evaluation metric to measure the individual contribution of each ingredient to the effectiveness of the prompt.
3. Replace parts of the path dynamically in runtime, for example injecting (retrieval) augmentation info into the prompt, changing rules based on user's permissions and context, and more.

To see how a Path is contstructed, please see [Path](docs/path.md).

# TODO items: 

<details>
<summary> List of TODOs. Click to expand. </summary>

- [ ] f-string based template combinator
- [ ] Consider improving support for templating fields as output (i.e. the output contains a template field that needs to be filled by the user)
- [ ] Add runtime extension outlets (e.g. for adding a new child to a combinator at a named position at runtime)
- [ ] Add runtime usage documentation - creating, replacing/editing, rendering.
- [ ] Implement the evaluator
- [ ] Support nested templates
- [ ] Support shared context for combinators - where one combinator's path selection affects / enforces another's selection.
- [ ] Implement best practices templates according to model type, model, and task. 
- [ ] Implement a registry loader for pre-built combinators. 
- [ ] Consider adding support for LLMLingua compression.
- [ ] Add documentation regarding token counting, prompt distance, compression, and other optimization techniques.
- [ ] Add additional literature pointers showing the sensitivity of outcomes to minor variation in prompt (specifically find the separators article)
- [ ] Add vision model examples
- [ ] Document how context + filter / combinators can be used to filter only some examples to add to prompt in runtime.
- [ ] Partial application user story

</details>
<br/>


# Persistance

<details>
<summary>Click to expand</summary>
<br/>

## Persisting and loading the Combinator tree

The library supports JSON serialization and deserialization of the combinator tree. This allows you to save the tree to a file, and load it later to generate prompts. 

We recommend using JSON over pickle due to security concerns with pickle.

```python
        template_source = "{{role}}\n{{task}}\n{{question}}\n"
        template_combinator = Jinja2Template(
            template_source=template_source,
            children={
                "role": NamedString("role_id", "value_1"),
                "task": "task_value",
                "question": JoinSomeOf(
                    n_max=1,
                    n_min=1,
                    children=["option_1"],
                    separator="\n",
                    id="question_randomizer_1",
                ),
            },
            id="template_1",
        )

        # Persist to a JSON string
        json_str = template_combinator.to_json()

        # Store the JSON string to file
        with open("path/to/combinator.json", "w") as f:
            f.write(json_str)

        # Load the JSON string from file
        loaded_json_str = ""
        with open("path/to/combinator.json", "r") as f:
            loaded_json_str = f.read()

        # Load from the JSON string
        loaded_combinator = Combinator.from_json(loaded_json_str)

```

## Persisting and loading the rendered prompts

The rendered prompts are strings, and each associated Path is a simple dictionary, with no dependence on custom objects. 

This means we can simply serialize, store, load and deserialize the prompts using and serialization and storage of our choice without explicit support in the library. 

```python
# Render all combinations of the prompts and store them to a string
all_paths = template_combinator.generate_paths()
storage = []
for path in all_paths:
    prompt = root_combinator.render_path(path)
    storage.append((prompt, path))

serialized = json.dumps(storage)
```

A different method is to use the (`versioned-collection`)[https://github.com/RomansWorks/versioned-collection] library:

```bash
pip install versioned-collection    
```

```python
from versioned_collection import Collection, CollectionStore

collection = Collection(items=[Item(key="my.item", value="my item value")])
# Or add one by one
collection.add(Item(key="my.item", value="my item value"))

collection_store = CollectionStore(...)
collection_store.store(collection)
```

And then load in the target app using:

```python
from versioned_collection import CollectionStore

collection = CollectionStore.load(url="path/to/collection")
```

## Persisting and loading the combinator tree and rendered prompts together

- [ ] - TODO: Document using promptsfile 

</details>

# Full example

See [Full Example](examples/text2text/example.py) for a full example of how to use the library, or click below to expand.

## Full Example code

<details>
    <summary>Click to expand</summary>

```python

import random
from typing import List
from pcombinator.combinators import JoinSomeOf, NamedString, Jinja2Template, PickOne

import json
from rich import print, print_json


def main():

    # This example picks one named string of several
    # Named strings preserve the id in the Path, while regular strings do not
    role_combinator = PickOne(
        id="role_combinator",
        children=[
            NamedString(
                id="1", string="You're a highly precise language model assistant."
            ),
            NamedString(
                id="2",
                string="You're an expert teacher with creative approach to explaining.",
            ),
        ],
    )

    # This example picks one string of several
    task_combinator = PickOne(
        id="task_combinator",
        children=[
            "Your task is to explain concepts provided by the user on three levels - ELI5, intuitive and rigorous.",
            "Your task is to explain concepts provided by the user on three levels - beginner, intermediate, expert.",
            "Your task is to explain concepts provided by the user on three levels.",
        ],
    )

    tone_combinator = PickOne(
        id="tone_combinator",
        children=[
            "Use a friendly and supporive tone.",
            "Use clean and professional tone.",
            None,
        ],
    )

    step_by_step_combinator = PickOne(
        id="step_by_step_combinator",
        children=[
            """Use the following step by step instruction to answer the user query:
Step 1: Rephrase the user question or request.
Step 2: Answer the question or request.
""",
            """Follow these steps when answering the user query:
Step 1: Briefly rephrase the user question or request.
Step 2: Answer the question or request.
""",
            "Think step by step.",
            None,
        ],
    )

    # Example of generating a list of samples from a dict, and combining some of them with a separator
    examples_list = [
        {
            "question:": "Get all records from the employees table",
            "answer": "SELECT * FROM employees",
        },
        {
            "question:": 'Get the single customer with id "PCombinator"',
            "answer": "SELECT DISTINCT * FROM customers WHERE id = 'PCombinator'",
        },
        {
            "question:": "Get the top 10 customers by revenue",
            "answer": "SELECT * FROM customers ORDER BY revenue DESC LIMIT 10",
        },
    ]

    example_strings = [
        f"Question: {example['question:']}\nAnswer: {example['answer']}"
        for example in examples_list
    ]
    example_named_strings = [
        NamedString(id=str(idx), string=example)
        for idx, example in enumerate(example_strings)
    ]

    examples_combinator = JoinSomeOf(
        id="examples_combinator",
        n_min=1,
        n_max=3,
        separator="\n",
        children=example_named_strings,
    )

    # Tipping - a way to encourage the model to yield better responses
    tip_combinator = PickOne(
        id="tip_combinator",
        children=[
            "I'm going to tip $1 for a perfect response!",
            "I'm going to tip $10 for a perfect response!",
            "I'm going to tip $100 for a perfect response!",
            None,
        ],
    )

    # This example is for using a Jinja2 template to combine the strings
    root_combinator = Jinja2Template(
        id="root",
        template_source="""
{{ role }}
{{ task }}
{{ tone }}
{{ step_by_step }}
{{ tip }}
Examples:
====
{{ examples }}
""",
        children={
            "role": role_combinator,
            "task": task_combinator,
            "tone": tone_combinator,
            "step_by_step": step_by_step_combinator,
            "tip": tip_combinator,
            "examples": examples_combinator,
        },
    )

    paths = root_combinator.generate_paths()
    n_samples = 5
    # Pick 5 samples in random
    selected_paths = random.sample(paths, n_samples)
    for idx, path in enumerate(selected_paths):
        rendered_prompt = root_combinator.render_path(path)
        print(
            f"\U000027A1 [bold blue] Candidate prompt [/bold blue][bold white]{idx}[/bold white]: "
        )
        print(f"[yellow] {rendered_prompt} [/yellow]")
        print()
        print(
            f"\U000027A1 [bold blue] Candidate ingredients (Path) for prompt [/bold blue][bold white]{idx}[/bold white]:"
        )
        pretty_path = json.dumps(path, indent=2)
        print_json(pretty_path)
        print("=" * 80)


# Main
if __name__ == "__main__":
    main()
```

</details>

## Example output

<details>
    <summary>Click to expand</summary>

```bash
➡  Candidate prompt 0: 
 
You're an expert teacher with creative approach to explaining.
Your task is to explain concepts provided by the user on three levels - ELI5, intuitive and rigorous.
Use clean and professional tone.
Use the following step by step instruction to answer the user query:
Step 1: Rephrase the user question or request.
Step 2: Answer the question or request.

I'm going to tip $100 for a perfect response!
Examples:
====
Question: Get the top 10 customers by revenue
Answer: SELECT * FROM customers ORDER BY revenue DESC LIMIT 10
Question: Get the single customer with id "PCombinator"
Answer: SELECT DISTINCT * FROM customers WHERE id = 'PCombinator'
Question: Get all records from the employees table
Answer: SELECT * FROM employees 

➡  Candidate ingredients (Path) for prompt 0:
{
  "root": {
    "role": {
      "role_combinator": {
        "1": {
          "2": {}
        }
      }
    },
    "task": {
      "task_combinator": {
        "0": "Your task is to explain concepts provided by the user on three levels - ELI5, intuitive and rigorous."
      }
    },
    "tone": {
      "tone_combinator": {
        "1": "Use clean and professional tone."
      }
    },
    "step_by_step": {
      "step_by_step_combinator": {
        "0": "Use the following step by step instruction to answer the user query:\nStep 1: Rephrase the user question or request.\nStep 2: Answer the question or request.\n"
      }
    },
    "tip": {
      "tip_combinator": {
        "2": "I'm going to tip $100 for a perfect response!"
      }
    },
    "examples": {
      "examples_combinator": {
        "2": {
          "2": {}
        },
        "1": {
          "1": {}
        },
        "0": {
          "0": {}
        }
      }
    }
  }
}
================================================================================
➡  Candidate prompt 1: 
 
You're a highly precise language model assistant.
Your task is to explain concepts provided by the user on three levels.



Examples:
====
Question: Get the single customer with id "PCombinator"
Answer: SELECT DISTINCT * FROM customers WHERE id = 'PCombinator'
Question: Get all records from the employees table
Answer: SELECT * FROM employees
Question: Get the top 10 customers by revenue
Answer: SELECT * FROM customers ORDER BY revenue DESC LIMIT 10 

➡  Candidate ingredients (Path) for prompt 1:
{
  "root": {
    "role": {
      "role_combinator": {
        "0": {
          "1": {}
        }
      }
    },
    "task": {
      "task_combinator": {
        "2": "Your task is to explain concepts provided by the user on three levels."
      }
    },
    "tone": {
      "tone_combinator": {
        "2": {}
      }
    },
    "step_by_step": {
      "step_by_step_combinator": {
        "3": {}
      }
    },
    "tip": {
      "tip_combinator": {
        "3": {}
      }
    },
    "examples": {
      "examples_combinator": {
        "1": {
          "1": {}
        },
        "0": {
          "0": {}
        },
        "2": {
          "2": {}
        }
      }
    }
  }
}
================================================================================
➡  Candidate prompt 2: 
 
You're an expert teacher with creative approach to explaining.
Your task is to explain concepts provided by the user on three levels.
Use a friendly and supporive tone.
Follow these steps when answering the user query:
Step 1: Briefly rephrase the user question or request.
Step 2: Answer the question or request.

I'm going to tip $1 for a perfect response!
Examples:
====
Question: Get the single customer with id "PCombinator"
Answer: SELECT DISTINCT * FROM customers WHERE id = 'PCombinator'
Question: Get all records from the employees table
Answer: SELECT * FROM employees 

➡  Candidate ingredients (Path) for prompt 2:
{
  "root": {
    "role": {
      "role_combinator": {
        "1": {
          "2": {}
        }
      }
    },
    "task": {
      "task_combinator": {
        "2": "Your task is to explain concepts provided by the user on three levels."
      }
    },
    "tone": {
      "tone_combinator": {
        "0": "Use a friendly and supporive tone."
      }
    },
    "step_by_step": {
      "step_by_step_combinator": {
        "1": "Follow these steps when answering the user query:\nStep 1: Briefly rephrase the user question or request.\nStep 2: Answer the question or request.\n"
      }
    },
    "tip": {
      "tip_combinator": {
        "0": "I'm going to tip $1 for a perfect response!"
      }
    },
    "examples": {
      "examples_combinator": {
        "1": {
          "1": {}
        },
        "0": {
          "0": {}
        }
      }
    }
  }
}
================================================================================
➡  Candidate prompt 3: 
 
You're an expert teacher with creative approach to explaining.
Your task is to explain concepts provided by the user on three levels.
Use clean and professional tone.
Follow these steps when answering the user query:
Step 1: Briefly rephrase the user question or request.
Step 2: Answer the question or request.

I'm going to tip $1 for a perfect response!
Examples:
====
Question: Get the single customer with id "PCombinator"
Answer: SELECT DISTINCT * FROM customers WHERE id = 'PCombinator'
Question: Get the top 10 customers by revenue
Answer: SELECT * FROM customers ORDER BY revenue DESC LIMIT 10
Question: Get all records from the employees table
Answer: SELECT * FROM employees 

➡  Candidate ingredients (Path) for prompt 3:
{
  "root": {
    "role": {
      "role_combinator": {
        "1": {
          "2": {}
        }
      }
    },
    "task": {
      "task_combinator": {
        "2": "Your task is to explain concepts provided by the user on three levels."
      }
    },
    "tone": {
      "tone_combinator": {
        "1": "Use clean and professional tone."
      }
    },
    "step_by_step": {
      "step_by_step_combinator": {
        "1": "Follow these steps when answering the user query:\nStep 1: Briefly rephrase the user question or request.\nStep 2: Answer the question or request.\n"
      }
    },
    "tip": {
      "tip_combinator": {
        "0": "I'm going to tip $1 for a perfect response!"
      }
    },
    "examples": {
      "examples_combinator": {
        "1": {
          "1": {}
        },
        "2": {
          "2": {}
        },
        "0": {
          "0": {}
        }
      }
    }
  }
}
================================================================================
➡  Candidate prompt 4: 
 
You're an expert teacher with creative approach to explaining.
Your task is to explain concepts provided by the user on three levels - beginner, intermediate, expert.
Use clean and professional tone.
Use the following step by step instruction to answer the user query:
Step 1: Rephrase the user question or request.
Step 2: Answer the question or request.

I'm going to tip $10 for a perfect response!
Examples:
====
Question: Get the top 10 customers by revenue
Answer: SELECT * FROM customers ORDER BY revenue DESC LIMIT 10
Question: Get all records from the employees table
Answer: SELECT * FROM employees 

➡  Candidate ingredients (Path) for prompt 4:
{
  "root": {
    "role": {
      "role_combinator": {
        "1": {
          "2": {}
        }
      }
    },
    "task": {
      "task_combinator": {
        "1": "Your task is to explain concepts provided by the user on three levels - beginner, intermediate, expert."
      }
    },
    "tone": {
      "tone_combinator": {
        "1": "Use clean and professional tone."
      }
    },
    "step_by_step": {
      "step_by_step_combinator": {
        "0": "Use the following step by step instruction to answer the user query:\nStep 1: Rephrase the user question or request.\nStep 2: Answer the question or request.\n"
      }
    },
    "tip": {
      "tip_combinator": {
        "1": "I'm going to tip $10 for a perfect response!"
      }
    },
    "examples": {
      "examples_combinator": {
        "2": {
          "2": {}
        },
        "0": {
          "0": {}
        }
      }
    }
  }
}
================================================================================
```
</details>
<br/>


# Contributing and Developing

See [Developing](docs/developing.md) for more information on how to develop the library.
