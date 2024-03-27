package chainmaker

import (
	"fmt"
	"os"
	"strconv"
	"testing"

	cm "chainmaker.org/chainmaker/sdk-go/v2"
	"go.uber.org/zap"
)

var pool *ClusterPool = nil

type Cluster struct {
	chains map[string]*ChainMakerModel
	orgs   []string
}

func (c *Cluster) AsOrg(index int) *ChainMakerModel {
	return c.chains[c.orgs[index]]
}

func (c *Cluster) Org(index int) string {
	return c.orgs[index]
}

func (c *Cluster) Size() int {
	return len(c.orgs)
}

func (c *Cluster) EachOrg(t *testing.T, do func(t *testing.T, index int, org string, model *ChainMakerModel)) {
	for i, org := range c.orgs {
		model := c.chains[org]
		index := i + 1
		do(t, index, org, model)
	}
}

type ClusterPool struct {
	ch chan *Cluster
}

func (p *ClusterPool) Put(cluster *Cluster) {
	p.ch <- cluster
}

func (p *ClusterPool) Get() *Cluster {
	return <-p.ch
}

func (p *ClusterPool) Size() int {
	return len(p.ch)
}

func createClusters(count int, contractFmt, configPathFmt string) []*Cluster {
	logger, err := zap.NewDevelopment()
	if err != nil {
		panic("create logger failed: " + err.Error())
	}
	orgs := []string{
		"wx-org1.chainmaker.org",
		"wx-org2.chainmaker.org",
		"wx-org3.chainmaker.org",
		"wx-org4.chainmaker.org",
	}
	clients := []*cm.ChainClient{}
	for i := range orgs {
		index := i + 1
		configPath := fmt.Sprintf(configPathFmt, index)
		client, err := CreateClient(configPath)
		if err != nil {
			panic(fmt.Sprintf("create chain client failed, for config path %s: %s", configPath, err))
		}
		clients = append(clients, client)
	}

	clusters := []*Cluster{}

	for i := 0; i < count; i++ {
		index := i + 1
		contractName := fmt.Sprintf(contractFmt, index)
		chains := map[string]*ChainMakerModel{}
		for j, org := range orgs {
			client := clients[j]
			model := &ChainMakerModel{
				logger:       logger,
				contractName: contractName,
				client:       client,
			}
			chains[org] = model
		}
		clusters = append(clusters, &Cluster{
			chains: chains,
			orgs:   orgs,
		})
	}

	return clusters
}

func InitCluster() *ClusterPool {
	count := os.Getenv("PARALLEL_COUNT")
	var c int64
	var err error
	if count == "" {
		c = 1
	} else {
		c, err = strconv.ParseInt(count, 10, 64)
		if err != nil {
			panic(err)
		}
	}

	contractFmt := os.Getenv("CONTRACT_FMT")
	if contractFmt == "" {
		panic("can't find CONTRACT_FMT environment")
	}

	configPathFmt := os.Getenv("CONFIG_PATH_FMT")
	if configPathFmt == "" {
		panic("can't find CONFIG_PATH_FMT environment")
	}

	ch := make(chan *Cluster, c)
	for _, cl := range createClusters(int(c), contractFmt, configPathFmt) {
		ch <- cl
	}
	return &ClusterPool{ch}
}

func setup(t *testing.T) *Cluster {
	t.Helper()
	t.Parallel()
	cluster := pool.Get()
	t.Log("cluster fetched, contract: " + cluster.chains[cluster.Org(0)].contractName)
	err := cluster.AsOrg(0).ReInit()
	if err != nil {
		panic("reinit failed: " + err.Error())
	}
	return cluster
}

func teardown(t *testing.T, cluster *Cluster) {
	t.Helper()
	pool.Put(cluster)
}

func TestMain(m *testing.M) {
	pool = InitCluster()
	m.Run()
}
