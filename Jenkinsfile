pipeline {
  agent {
    dockerfile true
  }
  libraries {
    lib('fxtest@1.10')
  }
  environment {
    PROJECT = "${PROJECT ?: JOB_NAME.find('\\.') ? JOB_NAME.split('\\.')[0] : ''}"
    TEST_ENV = "${TEST_ENV ?: JOB_NAME.find('\\.') ? JOB_NAME.split('\\.')[1] : ''}"
    KINTO_QA = credentials('kintoqa')
    KINTO_DOTENV = credentials('KINTO_DOTENV')
  }
  triggers {
    pollSCM(env.BRANCH_NAME == 'master' ? 'H/5 * * * *' : '')
    cron(env.BRANCH_NAME == 'master' ? 'H H * * *' : '')
  }
  options {
    ansiColor('xterm')
    timestamps()
    timeout(time: 1, unit: 'HOURS')
  }
  stages {
    stage('Lint') {
      steps {
        sh "flake8"
      }
    }
    stage('Test') {
      parallel {
        stage('kinto-dist.stage') {
          when {
            anyOf {
              not { environment name: 'CHANGE_ID', value: '' }
              allOf {
                environment name: 'PROJECT', value: 'kinto';
                environment name: 'TEST_ENV', value: 'stage'
              }
            }
          }
          steps {
            sh "pytest -m dist --env=stage"
          }
        }
        stage('kinto-dist.prod') {
          when {
            anyOf {
              not { environment name: 'CHANGE_ID', value: '' }
              allOf {
                environment name: 'PROJECT', value: 'kinto';
                environment name: 'TEST_ENV', value: 'prod'
              }
            }
          }
          steps {
            sh "pytest -m dist --env=prod"
          }
        }
        stage('kintowe.stage') {
          when {
            anyOf {
              not { environment name: 'CHANGE_ID', value: '' }
              allOf {
                environment name: 'PROJECT', value: 'kintowe';
                environment name: 'TEST_ENV', value: 'stage'
              }
            }
          }
          steps {
            sh "pytest -m webextensions --env=stage"
          }
        }
        stage('kintowe.prod') {
          when {
            anyOf {
              not { environment name: 'CHANGE_ID', value: '' }
              allOf {
                environment name: 'PROJECT', value: 'kintowe';
                environment name: 'TEST_ENV', value: 'prod'
              }
            }
          }
          steps {
            sh "pytest -m webextensions --env=prod"
          }
        }
      }
    }
  }
  post {
    failure {
      ircNotification('#storage')
      ircNotification('#fx-test-alerts')
      emailext(
        attachLog: true,
        body: '$BUILD_URL\n\n$FAILED_TESTS',
        replyTo: '$DEFAULT_REPLYTO',
        subject: '$DEFAULT_SUBJECT',
        to: '$DEFAULT_RECIPIENTS')
    }
  }
}
