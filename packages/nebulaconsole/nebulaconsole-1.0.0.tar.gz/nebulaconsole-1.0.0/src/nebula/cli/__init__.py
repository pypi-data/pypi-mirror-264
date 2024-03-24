import nebula.settings
from nebula._internal.compatibility.experimental import experiment_enabled
from nebula.cli.root import app

# Import CLI submodules to register them to the app
# isort: split

import nebula.cli.agent
import nebula.cli.artifact
import nebula.cli.block
import nebula.cli.cloud
import nebula.cli.cloud.webhook
import nebula.cli.concurrency_limit
import nebula.cli.config
import nebula.cli.deploy
import nebula.cli.deployment
import nebula.cli.dev
import nebula.cli.flow
import nebula.cli.flow_run
import nebula.cli.kubernetes
import nebula.cli.profile
import nebula.cli.project
import nebula.cli.server
import nebula.cli.variable
import nebula.cli.work_pool
import nebula.cli.work_queue
import nebula.cli.worker
import nebula.cli.task_run
