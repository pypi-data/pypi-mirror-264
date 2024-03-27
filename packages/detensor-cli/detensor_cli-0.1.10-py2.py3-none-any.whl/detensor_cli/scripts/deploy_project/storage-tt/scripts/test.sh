#! /usr/bin/env bash

tests=(
  "test_insert_table"
  "test_insert_index"
)

invoke_test() {
  ./cmc client contract user invoke \
    --contract-name=example \
    --method=$1 \
    --sdk-conf-path=./sdk_config.yml \
    --sync-result=true
}

cnt=1
total=${#tests[@]}
failed=0
passed=0

for test in ${tests[@]}; do
  echo [$cnt/$total] "now test" $test
  ((cnt += 1))

  invoke_test $test | grep "ERROR"

  if [ $? = 0 ]; then
    echo "failed"
    ((failed += 1))
  else
    echo "passed"
    ((passed += 1))
  fi
done

echo "Summary: $passed passed, $failed failed"
