package test

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

var cluster *Cluster = nil

func init() {
	cluster = LocalCluster()
}

// TestRegisterNode 测试注册计算节点地址的功能, 和按组织查询节点地址的功能
func TestRegisterNode(t *testing.T) {
	cluster.ReInit()
	resp, err := cluster.PostRawJson(0, "/api/core/v1/nodes/", []byte(`
		{
			"addr": "http://example-addr1"
		}
	`), nil)

	assert.Nilf(t, err, "register failed")
	assert.Equalf(t, http.StatusOK, resp.StatusCode, "register error")

	for i := 0; i < cluster.Size(); i++ {
		resp, err = cluster.Get(i, "/api/core/v1/nodes/", []Query{
			{
				Key:   "orgs",
				Value: cluster.Org(0),
			},
		})

		assert.Nilf(t, err, "get address failed")
		assert.Equalf(t, http.StatusOK, resp.StatusCode, "get address error")

		bytes, err := io.ReadAll(resp.Body)
		assert.Nilf(t, err, "read body failed")
		assert.JSONEq(t, fmt.Sprintf(`{"%s": "http://example-addr1"}`, cluster.Org(0)), string(bytes))
	}

}

// TestLogoutNode 测试注销计算节点地址的功能
func TestLogoutNode(t *testing.T) {
	cluster.ReInit()
	resp, err := cluster.PostRawJson(0, "/api/core/v1/nodes/", []byte(`
		{
			"addr": "http://example-addr1"
		}
	`), nil)

	assert.Nilf(t, err, "register failed")
	assert.Equalf(t, http.StatusOK, resp.StatusCode, "register error")

	resp, err = cluster.Delete(0, "/api/core/v1/nodes/", nil)
	assert.Nilf(t, err, "logout failed")
	assert.Equalf(t, http.StatusOK, resp.StatusCode, "logout error")

	for i := 0; i < cluster.Size(); i++ {
		resp, err = cluster.Get(i, "/api/core/v1/nodes/", []Query{
			{
				Key:   "orgs",
				Value: cluster.Org(0),
			},
		})

		assert.Nilf(t, err, "get address failed")
		assert.Equalf(t, http.StatusOK, resp.StatusCode, "get address error")

		bytes, err := io.ReadAll(resp.Body)
		assert.Nilf(t, err, "read body failed")
		assert.JSONEq(t, `{}`, string(bytes))
	}
}

// TestDiscoverAll 测试查询所有计算节点地址的功能
func TestDiscoverAll(t *testing.T) {
	cluster.ReInit()

	// 预计结果
	expect := map[string]string{}

	// 每个组织都进行注册
	for i := 0; i < cluster.Size(); i++ {
		addr := fmt.Sprintf("http://example-addr%d", i+1)
		expect[cluster.Org(i)] = addr

		resp, err := cluster.PostJson(i, "/api/core/v1/nodes/", gin.H{
			"addr": addr,
		}, nil)
		assert.Nilf(t, err, "register failed")
		assert.Equalf(t, http.StatusOK, resp.StatusCode, "register error")
	}

	// 预计结果进行JSON编码
	expectBytes, err := json.Marshal(expect)
	if err != nil {
		panic(err)
	}

	// 在每个组织上测试查询所有节点的结果
	for i := 0; i < cluster.Size(); i++ {
		resp, err := cluster.Get(i, "/api/core/v1/nodes/", nil)
		assert.Nilf(t, err, "get address failed")
		assert.Equalf(t, http.StatusOK, resp.StatusCode, "get address error")

		bytes, err := io.ReadAll(resp.Body)
		assert.Nilf(t, err, "read body failed")
		assert.JSONEq(t, string(expectBytes), string(bytes))
	}
}
