package chainmaker

import (
	"fmt"

	cm "chainmaker.org/chainmaker/sdk-go/v2"
	"go.uber.org/zap"
)

type ChainMakerModel struct {
	logger       *zap.Logger
	contractName string
	client       *cm.ChainClient
}

func NewChainMakerModel(contractName string, clientConfigPath string) (*ChainMakerModel, error) {
	logger, err := zap.NewDevelopment()
	if err != nil {
		return nil, err
	}

	client, err := CreateClient(clientConfigPath)
	if err != nil {
		return nil, err
	}
	return &ChainMakerModel{
		contractName: contractName,
		client:       client,
		logger:       logger,
	}, nil
}

func (m *ChainMakerModel) ProviderName() (string, error) {
	cfg, err := m.client.GetChainConfig()
	if err != nil {
		return "", err
	}
	version := cfg.GetVersion()
	return fmt.Sprintf("chainmaker-%s", version), nil
}

func (m *ChainMakerModel) GetAllOrg() ([]string, error) {
	cfg, err := m.client.GetChainConfig()
	if err != nil {
		return nil, err
	}

	ret := []string{}
	nodes := cfg.Consensus.Nodes
	for _, n := range nodes {
		orgId := n.GetOrgId()
		same := false
		for _, o := range ret {
			if orgId == o {
				same = true
			}
		}
		if !same {
			ret = append(ret, orgId)
		}
	}
	return ret, nil
}
