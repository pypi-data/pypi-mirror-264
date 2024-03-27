package test

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"path"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/require"
)

type Query struct {
	Key   string
	Value string
}

// Cluster 一个完整的存储层测试环境或Mock
type Cluster struct {
	// 组织名到对应的存储层API的根URL的字典
	addrs map[string]*url.URL

	// 集群中所有的组织名
	orgs []string
}

func LocalCluster() *Cluster {

	org1, err := url.Parse("http://localhost:9001/")
	if err != nil {
		panic(err)
	}

	org2, err := url.Parse("http://localhost:9002/")
	if err != nil {
		panic(err)
	}

	org3, err := url.Parse("http://localhost:9003/")
	if err != nil {
		panic(err)
	}

	org4, err := url.Parse("http://localhost:9004/")
	if err != nil {
		panic(err)
	}

	return &Cluster{
		addrs: map[string]*url.URL{
			"wx-org1.chainmaker.org": org1,
			"wx-org2.chainmaker.org": org2,
			"wx-org3.chainmaker.org": org3,
			"wx-org4.chainmaker.org": org4,
		},

		orgs: []string{
			"wx-org1.chainmaker.org",
			"wx-org2.chainmaker.org",
			"wx-org3.chainmaker.org",
			"wx-org4.chainmaker.org",
		},
	}
}

func JoinPath(u *url.URL, elem ...string) *url.URL {
	u.Path = path.Join(elem...)
	return u
}

func (c *Cluster) Size() int {
	return len(c.orgs)
}

func (c *Cluster) Org(n int) string {
	return c.orgs[n]
}

func (c *Cluster) BaseURL(n int) *url.URL {
	return c.addrs[c.Org(n)]
}

func (c *Cluster) BaseURLByName(name string) *url.URL {
	return c.addrs[name]
}

func (c *Cluster) Get(n int, path string, querys []Query) (*http.Response, error) {
	baseUrl := c.BaseURL(n)
	JoinPath(baseUrl, path)

	for _, v := range querys {
		baseUrl.Query().Add(v.Key, v.Value)
	}
	return http.Get(baseUrl.String())
}

func (c *Cluster) Delete(n int, path string, querys []Query) (*http.Response, error) {
	baseUrl := c.BaseURL(n)
	JoinPath(baseUrl, path)

	for _, v := range querys {
		baseUrl.Query().Add(v.Key, v.Value)
	}

	req, err := http.NewRequest(http.MethodDelete, baseUrl.String(), nil)
	if err != nil {
		return nil, err
	}

	return http.DefaultClient.Do(req)
}

func (c *Cluster) PostJson(n int, path string, body interface{}, querys []Query) (*http.Response, error) {
	out, err := json.Marshal(body)
	if err != nil {
		return nil, err
	}

	return c.PostRawJson(n, path, out, querys)
}

func (c *Cluster) PostRawJson(n int, path string, body []byte, querys []Query) (*http.Response, error) {
	baseUrl := c.BaseURL(n)
	JoinPath(baseUrl, path)
	for _, v := range querys {
		baseUrl.Query().Add(v.Key, v.Value)
	}

	return http.Post(baseUrl.String(), "application/json", bytes.NewReader(body))
}

func (c *Cluster) PutPlainText(n int, path, body string, querys []Query) (*http.Response, error) {
	baseUrl := c.BaseURL(n)
	JoinPath(baseUrl, path)
	for _, v := range querys {
		baseUrl.Query().Add(v.Key, v.Value)
	}

	req, err := http.NewRequest(http.MethodPut, baseUrl.String(), strings.NewReader(body))
	if err != nil {
		return nil, err
	}

	req.Header.Add("Content-Type", "text/plain")

	return http.DefaultClient.Do(req)
}

func (c *Cluster) PutRawJson(n int, path string, json []byte, querys []Query) (*http.Response, error) {
	baseUrl := c.BaseURL(n)
	JoinPath(baseUrl, path)
	for _, v := range querys {
		baseUrl.Query().Add(v.Key, v.Value)
	}

	req, err := http.NewRequest(http.MethodPut, baseUrl.String(), bytes.NewReader(json))
	if err != nil {
		return nil, err
	}

	req.Header.Add("Content-Type", "application/json")

	return http.DefaultClient.Do(req)
}

func (c *Cluster) PutJson(n int, path string, querys []Query, body interface{}) (*http.Response, error) {

	json, err := json.Marshal(body)
	if err != nil {
		return nil, err
	}

	baseUrl := c.BaseURL(n)
	JoinPath(baseUrl, path)
	for _, v := range querys {
		baseUrl.Query().Add(v.Key, v.Value)
	}

	req, err := http.NewRequest(http.MethodPut, baseUrl.String(), bytes.NewReader(json))
	if err != nil {
		return nil, err
	}

	req.Header.Add("Content-Type", "application/json")

	return http.DefaultClient.Do(req)
}

func (c *Cluster) ReInit() {
	resp, err := c.Delete(0, "/api/core/v1/debug", nil)
	if err != nil {
		log.Fatalf("ReInit failed: %s", err.Error())
	}
	if resp.StatusCode != http.StatusOK {
		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatalf("ReInit failed, status code: %d, read resp body failed: %s", resp.StatusCode, err.Error())
		}
		log.Fatalf("ReInit failed, status code: %d, resp: %s", resp.StatusCode, string(body))
	}
}

func ReadTestData(t *testing.T, caseName, path string) []byte {
	t.Helper()
	fullpath := filepath.Join("testdata/case", caseName, path)
	content, err := ioutil.ReadFile(fullpath)
	require.NoErrorf(t, err, "read testdata from case %s, path %s failed", caseName, path)
	return content
}

func RequireHttpResp(t *testing.T, msg string, resp *http.Response, err error, status int) []byte {
	t.Helper()
	if err != nil {
		t.Fatalf("%s: send http request failed, error: %s", msg, err.Error())
	}

	out, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		t.Fatalf("%s: read http respone body failed, error: %s", msg, err.Error())
	}

	require.Equalf(t, status, resp.StatusCode, "%s: http return status error, response body: %s", msg, string(out))
	return out
}
