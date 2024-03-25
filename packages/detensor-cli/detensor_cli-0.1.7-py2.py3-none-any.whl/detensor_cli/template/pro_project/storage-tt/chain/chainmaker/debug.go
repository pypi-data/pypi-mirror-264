// ChainMaker 调试用的链上接口, 这个文件仅在debug条件下被编入.

//go:build debug

package chainmaker

import (
	"fmt"
	"strconv"

	"chainmaker.org/chainmaker/pb-go/v2/common"
)

const (
	DEBUG_REINIT_METHOD_NAME  = "reinit_state"
	DEBUG_NEXTUID_METHOD_NAME = "next_uid"
)

func (m *ChainMakerModel) ReInit() error {
	resp, err := m.Invoke(DEBUG_REINIT_METHOD_NAME, []*common.KeyValuePair{}, "")
	if err != nil {
		return err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		return nil
	} else {
		return fmt.Errorf("debug reinit failed, code: %d, msg: %s", resp.Code, resp.ContractResult.Message)
	}
}

func (m *ChainMakerModel) NextUid() (uint64, error) {
	resp, err := m.Query(DEBUG_NEXTUID_METHOD_NAME, []*common.KeyValuePair{})
	if err != nil {
		return 0, err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		res := resp.ContractResult.Result
		ret, err := strconv.ParseUint(string(res), 10, 64)
		return ret, err
	} else {
		return 0, fmt.Errorf("debug nextuid failed, code: %d, msg: %s", resp.Code, resp.ContractResult.Message)
	}
}
