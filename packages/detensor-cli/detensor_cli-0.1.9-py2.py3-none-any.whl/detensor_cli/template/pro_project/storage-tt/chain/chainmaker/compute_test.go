package chainmaker

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestRegisterNode(t *testing.T) {
	cluster := setup(t)
	defer teardown(t, cluster)

	testUrl := "http://example-addr1"
	err := cluster.AsOrg(0).RegisterNode("http://example-addr1")
	require.NoErrorf(t, err, "register node failed")

	for i := 0; i < cluster.Size(); i++ {
		out, err := cluster.AsOrg(i).DiscoverNodes([]string{cluster.Org(0)})
		require.NoErrorf(t, err, "find node from org %d failed", i)
		require.Equalf(t, map[string]string{cluster.Org(0): testUrl}, out, "register failed")
	}
}

func TestLogoutNode(t *testing.T) {
	cluster := setup(t)
	defer teardown(t, cluster)

	testUrl := "http://example-addr1"
	err := cluster.AsOrg(0).RegisterNode(testUrl)
	require.NoErrorf(t, err, "register failed")

	err = cluster.AsOrg(0).LogoutNode()
	require.NoErrorf(t, err, "logout failed")

	cluster.EachOrg(t, func(t *testing.T, index int, org string, model *ChainMakerModel) {
		out, err := model.DiscoverAllNodes()
		require.NoErrorf(t, err, "discover all nodes failed")
		require.Equalf(t, map[string]string{}, out, "logout failed")
	})
}

func TestDiscoverAll(t *testing.T) {
	cluster := setup(t)
	defer teardown(t, cluster)

	expect := map[string]string{}
	for i := 0; i < cluster.Size(); i++ {
		addr := fmt.Sprintf("http://example-addr%d", i+1)
		expect[cluster.Org(i)] = addr
		err := cluster.AsOrg(i).RegisterNode(addr)
		require.NoErrorf(t, err, "register node failed")
	}

	for i := 0; i < cluster.Size(); i++ {
		out, err := cluster.AsOrg(i).DiscoverAllNodes()
		require.NoErrorf(t, err, "discover all failed")
		require.Equalf(t, expect, out, "discover all error")
	}
}
