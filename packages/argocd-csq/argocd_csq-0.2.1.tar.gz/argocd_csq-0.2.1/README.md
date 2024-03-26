# Argo CD CSQ

This is the new CS tool for managing Argo CD written in python.

# How to build
To install this tool, simply use the following command

```
pip install argocd-csq
```

# How to run
To run argocd-csq, you need to simply use the following command

```
argocd_csq
```

> **_NOTE:_**  It is very important to note that the first run of the tool will take sometime as it has to initialize some values and download some extra dependencies

After running the above command, you will see an output that will show you exactly how to run this tool.

The first thing that you need to do is to login via the command
```
argocd_csq login
```

This command will output an argocd authorization token that will be used when executing any argocd command.