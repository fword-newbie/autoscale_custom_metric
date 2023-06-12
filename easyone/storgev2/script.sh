    #!/bin/sh
    yaml_file=$1

    sudo kubectl apply -f $yaml_file
    