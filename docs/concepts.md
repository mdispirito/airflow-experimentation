DAG - Description of how to run a workflow.

Task - A unit of work within a DAG. There are dependencies between tasks.

Operator - Determine what gets done by a Task. Each task is an implementation of an Operator.

Execution Date - The launch date of a DAG.

Task Instance - The run of a task at a specific point in time.

DAG Run - An instantiation of a DAG containing Task Instances for a specific Execution Date.

Sensor - Type of Operator that waits for something to occur. Used when you don't know when something will happen or when data will be available.