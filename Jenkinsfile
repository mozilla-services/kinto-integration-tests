pipeline {
  agent {
    dockerfile true
  }
  libraries {
    lib('fxtest@1.10')
  }
  environment {
    PROJECT = "${PROJECT ?: JOB_NAME.split('\\.')[0]}"
    TEST_ENV = "${TEST_ENV ?: JOB_NAME.split('\\.')[1]}"
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
    stage('Test kinto-dist') {
      when {
        environment name: 'PROJECT', value: 'kinto'
      }
      steps {
        sh "pytest -m dist --env=${TEST_ENV}"
      }
    }
    stage('Test kintowe') {
      when {
        environment name: 'PROJECT', value: 'kintowe'
      }
      steps {
        sh "pytest -m webextensions --env=${TEST_ENV}"
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
