#!/bin/bash

rqworker ansible --exception-handler "lib.tasks.handle_task_exception"
