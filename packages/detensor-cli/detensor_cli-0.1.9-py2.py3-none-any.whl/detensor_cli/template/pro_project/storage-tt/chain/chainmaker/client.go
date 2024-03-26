package chainmaker

import (
	"fmt"

	"chainmaker.org/chainmaker/pb-go/v2/common"
	cm "chainmaker.org/chainmaker/sdk-go/v2"
	"go.uber.org/zap"
)

func CreateClient(configPath string) (*cm.ChainClient, error) {
	chainClient, err := cm.NewChainClient(
		cm.WithConfPath(configPath),
	)
	if err != nil {
		return nil, err
	}

	err = chainClient.EnableCertHash()
	if err != nil {
		return nil, err
	}

	return chainClient, nil
}

func Load(client *cm.ChainClient, key []byte) ([]byte, error) {
	params := []*common.KeyValuePair{
		{
			Key:   "key",
			Value: key,
		},
	}
	resp, err := client.QueryContract("example", "load", params, -1)
	if err != nil {
		return nil, err
	}

	if resp.Code != common.TxStatusCode_SUCCESS {
		return nil, fmt.Errorf("invoke contract failed, code:%d, msg:%s", resp.Code, resp.Message)
	}

	ret := resp.ContractResult.Result
	return ret, nil
}

func Save(client *cm.ChainClient, key, value []byte) error {
	params := []*common.KeyValuePair{
		{
			Key:   "key",
			Value: key,
		},
		{
			Key:   "value",
			Value: value,
		},
	}

	resp, err := client.InvokeContract("example", "save", "", params, -1, true)
	if err != nil {
		return err
	}

	if resp.Code != common.TxStatusCode_SUCCESS {
		return fmt.Errorf("invoke contract failed, code:%d, msg:%s", resp.Code, resp.Message)
	}
	return nil
}

func (m *ChainMakerModel) Invoke(method string, params []*common.KeyValuePair, txId string) (*common.TxResponse, error) {
	m.logger.Debug("Contract Invoke", zap.String("method", method), zap.String("txId", txId))
	return m.client.InvokeContract(m.contractName, method, txId, params, -1, true)
}

func (m *ChainMakerModel) Query(method string, params []*common.KeyValuePair) (*common.TxResponse, error) {
	m.logger.Debug("Contract Query", zap.String("method", method))
	return m.client.QueryContract(m.contractName, method, params, -1)
}
