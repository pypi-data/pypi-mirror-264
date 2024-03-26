package chainmaker

import (
	"encoding/json"
	"fmt"

	"buaa.edu.cn/storage/objects"
	"chainmaker.org/chainmaker/pb-go/v2/common"
)

const (
	REGISTER_NODE_METHOD_NAME      = "register_node"
	LOGOUT_NODE_METHOD_NAME        = "logout_node"
	DISCOVER_NODES_METHOD_NAME     = "discover_nodes"
	DISCOVER_ALL_NODES_METHOD_NAME = "discover_all_nodes"
	GET_CONTRACT_METHOD_NAME       = "get_contract"
)

func (m *ChainMakerModel) RegisterNode(addr string) error {
	params := []*common.KeyValuePair{
		{
			Key:   "addr",
			Value: []byte(addr),
		},
	}

	resp, err := m.Invoke(REGISTER_NODE_METHOD_NAME, params, "")
	if err != nil {
		return fmt.Errorf("invoke contract %s:%s failed: %w", m.contractName, REGISTER_NODE_METHOD_NAME, err)
	}

	if resp.Code != common.TxStatusCode_SUCCESS {
		return fmt.Errorf("invoke contract %s:%s error, code: %d, msg:%s", m.contractName, REGISTER_NODE_METHOD_NAME, resp.Code, resp.Message)
	}
	return nil
}

func (m *ChainMakerModel) LogoutNode() error {
	params := []*common.KeyValuePair{}
	resp, err := m.Invoke(LOGOUT_NODE_METHOD_NAME, params, "")
	if err != nil {
		return fmt.Errorf("invoke contract %s:%s failed: %w", m.contractName, LOGOUT_NODE_METHOD_NAME, err)
	}

	if resp.Code != common.TxStatusCode_SUCCESS {
		return fmt.Errorf("invoke contract %s:%s error, code: %d, msg:%s", m.contractName, LOGOUT_NODE_METHOD_NAME, resp.Code, resp.Message)
	}
	return nil
}

func (m *ChainMakerModel) DiscoverNodes(orgs []string) (map[string]string, error) {
	rawOrgs, err := json.Marshal(orgs)
	if err != nil {
		return nil, err
	}
	params := []*common.KeyValuePair{
		{
			Key:   "orgs",
			Value: rawOrgs,
		},
	}
	resp, err := m.Query(DISCOVER_NODES_METHOD_NAME, params)
	if err != nil {
		return nil, err
	}

	if resp.Code != common.TxStatusCode_SUCCESS {
		return nil, fmt.Errorf("query contract %s:%s failed, code:%d, msg:%s", m.contractName, DISCOVER_NODES_METHOD_NAME, resp.Code, resp.Message)
	}

	rawResult := resp.ContractResult.Result
	ret := map[string]string{}
	err = json.Unmarshal(rawResult, &ret)
	return ret, err
}

func (m *ChainMakerModel) DiscoverAllNodes() (map[string]string, error) {
	params := []*common.KeyValuePair{}
	resp, err := m.Query(DISCOVER_ALL_NODES_METHOD_NAME, params)
	if err != nil {
		return nil, err
	}

	if resp.Code != common.TxStatusCode_SUCCESS {
		return nil, fmt.Errorf("query contract %s:%s failed, code:%d, msg:%s", m.contractName, DISCOVER_ALL_NODES_METHOD_NAME, resp.Code, resp.Message)
	}

	rawResult := resp.ContractResult.Result
	ret := map[string]string{}
	err = json.Unmarshal(rawResult, &ret)
	return ret, err
}

func (m *ChainMakerModel) GetContract(uid uint64) (*objects.GetContractRes, error) {
	params := []*common.KeyValuePair{
		{
			Key:   "uid",
			Value: EncodeUint64(uid),
		},
	}
	resp, err := m.Query(GET_CONTRACT_METHOD_NAME, params)
	if err != nil {
		return nil, err
	}

	if resp.Code != common.TxStatusCode_SUCCESS {
		return nil, fmt.Errorf("query contract %s:%d, msg:%s", GET_CONTRACT_METHOD_NAME, uid, resp.Message)
	}

	rawResult := resp.ContractResult.Result
	if rawResult == nil {
		return nil, nil
	}

	ret := &objects.GetContractRes{}
	err = json.Unmarshal(rawResult, ret)
	if err != nil {
		return nil, err
	}

	return ret, nil
}
