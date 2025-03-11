pipeline {
    agent any
    environment {
        ANSIBLE_HOST_KEY_CHECKING = 'False'
        PASSWORK_API_KEY = credentials('passwork-api-token')
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
        stage('Checkout Repository') {
            steps {
                git url: 'https://srv-glory.eurostil.ru/dmitry.shelokov/passwork-change-pw-root.git',
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
                        writeFile file: 'inventory.ini', text: inventory
                    }
                }
            }
        }
        stage('Run Ansible Playbook on Remote Servers') {
            steps {
                sh """
                ansible-playbook -i inventory.ini playbook.yml \
                    -e passwork_api_key=${PASSWORK_API_KEY}
                """
            }
        }
    }
}