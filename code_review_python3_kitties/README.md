# Requirements - verbatim from the recruiter
```
Please read:
 
In this mock assignment, you will be doing a code review for a junior engineer. 
This code will deploy to production immediately after merge. Make sure to 
check for functionality, quality, style, test coverage, typos, etc. We want to 
get a sense of your ability to read code, solve problems, and communicate to 
team members. We expect the review to be done in the current PR and not as an 
attachment, new folder, email, etc. Good luck!
```

# Feedback from the hiring company/self-assessment
No feedback. Company passed on me.

I suspect my code submission wasn't quite in line with expectations. While I wasn't explicitly invited - GitHub PR/assign code review - to review the existing PR, I submitted code changes, tests, and documentation as a feature branch. In retrospect, I should have sought clarification on the initial requirements before proceeding.

**_In the meantime - never mind the fact that I beta tested GitHub Actions in early 2018, and have since created custom GitHub actions. Have written thousands of lines of tooling using GitHub API etc._**

# Summary of my code submission

What you see in this branch is what I submitted. [Here are the diffs between my work and the original Main Branch](diffs_feature_remote_main.md)

The commits involved a range of tasks to improve code quality and readability. The first commit fixed a typo in the version variable, while subsequent commits focused on formatting and documentation. Variables were renamed to snake_case, and docstrings were added or clarified throughout the codebase. Exception handling was also improved, with empty list checks added to prevent errors. Testing was enhanced through the addition of test cases and output files, including details on test case results. Additionally, logging was implemented to provide a clearer understanding of code execution. Finally, commit updates included improvements to documentation, testing, and markdown formatting for run and diff outputs.

# Kitty Image Viewer

This utility code takes images of kitties and arranges them in nice rows.


## Local Development

### Setup

Ensure you're using python 3.10. If you use `pyenv` to manage python environments, run `pyenv version` to check. Run `pyenv global 3.10.0` to set 3.10.0 as the global version.

Create the virtual env so you have all the right versions of all the right packages. We'll use pipenv which integrations virtualenv and pip nicely.

1. `make setup-env` will install pipenv, dependencies. You can safely run this command multiple times.

### Development

To add a new dependency, use pipenv from within pipenv.

`pipenv run pipenv install NEW_DEP`

### Tests

`make test` will run all tests.

To run a single test, specify the package path.

Examples:

* `make test tests=tests.test_package` will run all tests in the `test_package` module.
* `make test tests=tests.test_package.TestClass.test_case` will just run the one test case.

### Running locally

`make run` or set flags like `make run flags="--page_width=100 --row_height=20"`. Use `make help` to see available flags.
