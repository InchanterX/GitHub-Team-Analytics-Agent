# Why this task?
I chose a task that can help me and other people solve a real problem that I encounter in my real work process — analysing the project repository of my team as a team leader. Sometimes we want to know what happened in a certain period of time, but we don't want to read through all the commits and issues, compare changes, and just want to see a summary of what has been done. So, my agent can help.

# The moments of failure
There were several moments that caused troubles.
The most significant of them were LLM hallucinations. It always tried to add something from itself. For instance, there was a problem: when the repository doesn't have any issues, the LLM tried to describe some non-existent issues that have never existed. Another time, the LLM was desperately trying to set the date of the most productive day to an impossible time. That problem was caused by the lack of information.

# Possible improvements
There are two significant things that I wanted to implement, but they were cut out in order to get everything done by the deadline.

1. Every big project uses organization functions to collect many related repositories, and it would be great to have the ability to search through all the repositories of an organization simultaneously. It can save even more time.
2. Not only GitHub exists, and it would be great to add GitLab connection. Using the current architecture, it would not be very hard to add such a function. All that is needed is to implement the GitLab API in adapters and add a choice between the two variants.

Apart from what was mentioned, there are, obviously, many other ways to improve the project. There are many options for how to extend the list of tools to analyze all kinds of things in repositories.