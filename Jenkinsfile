pipeline {
    agent any
    environment {
        ANSIBLE_HOST_KEY_CHECKING = 'False'
        PASSWORK_API_TOKEN = credentials('passwork-api-token')
    }
    parameters {
        string(name: 'REMOTE_IP_1', defaultValue: '192.168.111.82', description: 'IP адрес удаленного сервера 1')
        string(name: 'REMOTE_IP_2', defaultValue: '', description: 'IP адрес удаленного сервера 2')
        string(name: 'REMOTE_IP_3', defaultValue: '', description: 'IP адрес удаленного сервера 3')
        string(name: 'REMOTE_IP_4', defaultValue: '', description: 'IP адрес удаленного сервера 4')
        string(name: 'REMOTE_IP_5', defaultValue: '', description: 'IP адрес удаленного сервера 5')
    }
    stages {
        stage('Setup SSH') {
            steps {
                script {
                    def ips = [params.REMOTE_IP_1, params.REMOTE_IP_2, params.REMOTE_IP_3, params.REMOTE_IP_4, params.REMOTE_IP_5]
                    ips.each { ip ->
                        if (ip) {
                            sh "ssh-keygen -f /home/s2jnkans/.ssh/known_hosts -R ${ip} || true"
                            sh "ssh-keyscan -H ${ip} >> /home/s2jnkans/.ssh/known_hosts"
                        }
                    }
                }
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    sh """
                    sudo apt update || true
                    sudo apt install -y python3 python3-pip sshpass || true
                    pip3 install --upgrade pip
                    pip3 install -r ansible-project/requirements.txt
                    """
                }
            }
        }
        stage('Checkout Repository') {
            steps {
                git url: 'https://srv-glory.eurostil.ru/dmitry.shelokov/passwork-change-pw-root',
                    branch: 'main',
                    credentialsId: 'gitlab-credentials'
            }
        }
        stage('Generate Inventory') {
            steps {
                script {
                    def inventory = "[servers]\n"
                    withCredentials([usernamePassword(credentialsId: 'centos-video-srv-root', usernameVariable: 'REMOTE_USER', passwordVariable: 'REMOTE_PASSWORD')]) {
                        def ips = [params.REMOTE_IP_1, params.REMOTE_IP_2, params.REMOTE_IP_3, params.REMOTE_IP_4, params.REMOTE_IP_5]
                        ips.eachWithIndex { ip, index ->
                            if (ip) {
                                inventory += "srv-${index+1} ansible_host=${ip} ansible_user=${env.REMOTE_USER} ansible_ssh_pass=${env.REMOTE_PASSWORD}\n"
                            }
                        }
                        echo "Entered IP addresses: ${ips.join(', ')}"
                        writeFile file: 'ansible-project/inventory.ini', text: inventory
                    }
                }
            }
        }
        stage('Ensure Custom Modules are Available') {
            steps {
                script {
                    sh "mkdir -p ansible-project/library"
                    def moduleExists = sh(script: "[ -f ansible-project/library/passwork_add_password.py ] && echo 'true' || echo 'false'", returnStdout: true).trim()
                    if (moduleExists == "false") {
                        sh "cp ansible-project/modules/passwork_add_password.py ansible-project/library/"
                    }
                    sh "chmod +x ansible-project/library/passwork_add_password.py"
                    sh "ls -l ansible-project/library/passwork_add_password.py"
                }
            }
        }
        stage('Run Ansible Playbook on Remote Servers') {
            steps {
                sh """
                ansible-playbook -i ansible-project/inventory.ini ansible-project/playbooks/add_password.yml
                """
            }
        }
    }
}