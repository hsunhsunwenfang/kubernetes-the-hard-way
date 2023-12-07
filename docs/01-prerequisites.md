# Prerequisites

## Azure

This tutorial leverages the [Azure](https://azure.microsoft.com/en-us/) to streamline provisioning of the compute infrastructure required to bootstrap a Kubernetes cluster from the ground up. [Sign up](https://azure.microsoft.com/en-us/free/) for $200 in free credits.

[Estimated cost](https://azure.microsoft.com/en-us/pricing/calculator/) to run this tutorial: $0.23 per hour ($5.50 per day).

> The compute resources required for this tutorial exceed the Azure free tier.

## Azure CLI

### Install the Azure CLI

Follow the Azure CLI [documentation](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) to install and configure the `az` command line utility.

Verify the Azure CLI version is 2.0.80 or higher:

```
az --version
```

### Set a Default Compute Region and Zone

This tutorial assumes a default compute region and zone have been configured.

If you are using the `az` command-line tool for the first time `init` is the easiest way to do this:

```
az login
```

Then be sure to authorize az to access the Cloud Platform with your Azure user credentials:

```

Next set a default compute region and compute zone:

```

Set a default compute zone:

```

> Use the `az account list-locations` command to view additional regions and zones.

## Running Commands in Parallel with tmux



> The use of tmux is optional and not required to complete this tutorial.

![tmux screenshot](images/tmux-screenshot.png)


Next: [Installing the Client Tools](02-client-tools.md)
