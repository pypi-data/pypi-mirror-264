package test

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"github.com/tidwall/gjson"
)

func TestCreateNamespace(t *testing.T) {
	cluster.ReInit()

	// 首先创建构造命名空间的提议
	dir, _ := os.Getwd()
	println(dir)
	CREATE_NS_PROPOSAL, err := ioutil.ReadFile("testdata/case/namespace/create_proposal.json")
	assert.Nilf(t, err, "get ns proposal failed")

	resp, err := cluster.PostRawJson(0, "/api/core/v1/globalproposal/", []byte(CREATE_NS_PROPOSAL), nil)
	if err != nil {
		t.Fatalf("create global proposal failed, %s", err.Error())
	}

	assert.Equalf(t, http.StatusCreated, resp.StatusCode, "create globalproposal failed")

	content, err := ioutil.ReadAll(resp.Body)
	assert.Nilf(t, err, "read create response failed")

	var uid uint64
	err = json.Unmarshal(content, &uid)
	assert.Nilf(t, err, "parse returned uid failed")

	// 对提议进行批准
	for i := 0; i < 3; i++ {
		resp, err = cluster.PutPlainText(
			i,
			fmt.Sprintf("/api/core/v1/globalproposal/%d/permission", uid),
			fmt.Sprintf("comment from org %d", i),
			nil,
		)
		assert.Nilf(t, err, "permit proposal from org %d, failed", i)

		out, err := ioutil.ReadAll(resp.Body)
		if assert.NoErrorf(t, err, "read permit response body failed") {
			assert.Equalf(t, http.StatusOK, resp.StatusCode, "permit proposal from org%d, failed %s", i, string(out))
		}
	}

	// 对提议进行提交
	resp, err = cluster.PutJson(
		0,
		fmt.Sprintf("/api/core/v1/globalproposal/%d/commit", uid),
		nil, nil,
	)
	assert.Nilf(t, err, "commit proposal from org %d, failed", 0)
	assert.Equalf(t, http.StatusOK, resp.StatusCode, "commit proposal failed")
}

func TestDeleteNamespace(t *testing.T) {
	cluster.ReInit()

	// 首先创建构造命名空间的提议
	dir, _ := os.Getwd()
	println(dir)
	CREATE_NS_PROPOSAL, err := ioutil.ReadFile("testdata/case/namespace/create_proposal.json")
	assert.Nilf(t, err, "get ns proposal failed")

	resp, err := cluster.PostRawJson(0, "/api/core/v1/globalproposal/", []byte(CREATE_NS_PROPOSAL), nil)
	if err != nil {
		t.Fatalf("create global proposal failed, %s", err.Error())
	}

	assert.Equalf(t, http.StatusCreated, resp.StatusCode, "create globalproposal failed")

	content, err := ioutil.ReadAll(resp.Body)
	assert.Nilf(t, err, "read create response failed")

	var uid uint64
	err = json.Unmarshal(content, &uid)
	assert.Nilf(t, err, "parse returned uid failed")

	// 对提议进行批准
	for i := 0; i < 3; i++ {
		resp, err = cluster.PutPlainText(
			i,
			fmt.Sprintf("/api/core/v1/globalproposal/%d/permission", uid),
			fmt.Sprintf("comment from org %d", i),
			nil,
		)
		assert.Nilf(t, err, "permit proposal from org %d, failed", i)

		out, err := ioutil.ReadAll(resp.Body)
		if assert.NoErrorf(t, err, "read permit response body failed") {
			assert.Equalf(t, http.StatusOK, resp.StatusCode, "permit proposal from org%d, failed %s", i, string(out))
		}
	}

	// 对提议进行提交
	resp, err = cluster.PutJson(
		0,
		fmt.Sprintf("/api/core/v1/globalproposal/%d/commit", uid),
		nil, nil,
	)
	require.Nilf(t, err, "commit proposal from org %d, failed", 0)
	require.Equalf(t, http.StatusOK, resp.StatusCode, "commit proposal failed")

	content, err = ioutil.ReadAll(resp.Body)
	require.NoErrorf(t, err, "read commit response body failed")
	t.Logf("create proposal commit: %s", content)
	nsUid := gjson.Get(string(content), "0.create.metadata.uid").Uint()
	t.Logf("new namespace uid: %d", nsUid)

	DELETE_NS_PROPOSAL, err := ioutil.ReadFile("testdata/case/namespace/delete_proposal.json")
	require.Nilf(t, err, "get delete ns proposal failed")

	deleteProposal := fmt.Sprintf(string(DELETE_NS_PROPOSAL), nsUid)
	t.Logf("delete proposal: %s", deleteProposal)

	resp, err = cluster.PostRawJson(0,
		"/api/core/v1/globalproposal/",
		[]byte(deleteProposal),
		nil,
	)
	require.NoErrorf(t, err, "create global proposal failed")
	content, err = ioutil.ReadAll(resp.Body)
	require.NoErrorf(t, err, "read create delete proposal failed")
	require.Equalf(t, http.StatusCreated, resp.StatusCode, "create globalproposal failed, body: %s", string(content))

	var deleteProposalUid uint64
	err = json.Unmarshal(content, &deleteProposalUid)
	require.NoErrorf(t, err, "parse returned uid failed")

	// 对删除提议进行批准
	for i := 0; i < 3; i++ {
		resp, err = cluster.PutPlainText(
			i,
			fmt.Sprintf("/api/core/v1/globalproposal/%d/permission", deleteProposalUid),
			fmt.Sprintf("comment from org %d", i),
			nil,
		)
		assert.Nilf(t, err, "permit proposal from org %d, failed", i)

		out, err := ioutil.ReadAll(resp.Body)
		if assert.NoErrorf(t, err, "read delete permit response body failed") {
			assert.Equalf(t, http.StatusOK, resp.StatusCode, "permit delete globalproposal from org%d, failed %s", i, string(out))
		}
	}
	resp, err = cluster.PutJson(
		0,
		fmt.Sprintf("/api/core/v1/globalproposal/%d/commit", deleteProposalUid),
		nil, nil,
	)
	assert.Nilf(t, err, "commit proposal from org %d, failed", 0)
	assert.Equalf(t, http.StatusOK, resp.StatusCode, "commit delete proposal failed")

	resp, err = cluster.Get(0, "/api/core/v1/namespace", nil)
	if assert.NoErrorf(t, err, "get namespaces failed") {
		out, err := ioutil.ReadAll(resp.Body)
		if assert.NoErrorf(t, err, "read get namespaces body failed", nil) {
			assert.JSONEqf(t, "[]", string(out), "namespace not deleted")
		}
	}

}
