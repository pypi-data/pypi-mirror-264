package chainmaker

import (
	"fmt"

	"chainmaker.org/chainmaker/pb-go/v2/common"
)

const (
	SET_FN_IMPL_METHOD_NAME         = "set_function_implement"
	SET_FN_IMPL_BY_NAME_METHOD_NAME = "set_function_implement_by_name"
)

func (m *ChainMakerModel) SetFunctionImplement(uid uint64, status bool, comment string) error {
	uidBytes := EncodeUint64(uid)
	statusBytes := EncodeBool(status)

	params := []*common.KeyValuePair{
		{
			Key:   "uid",
			Value: uidBytes,
		},
		{
			Key:   "status",
			Value: statusBytes,
		},
		{
			Key:   "comment",
			Value: []byte(comment),
		},
	}

	resp, err := m.Invoke(SET_FN_IMPL_METHOD_NAME, params, "")
	if err != nil {
		return err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		return nil
	} else {
		return fmt.Errorf("set function implement error, code: %d, msg: %s", resp.Code, resp.ContractResult.Message)
	}
}

func (m *ChainMakerModel) SetFunctionImplementByName(namespace, name string, status bool, comment string) error {
	statusBytes := EncodeBool(status)

	params := []*common.KeyValuePair{
		{
			Key:   "namespace",
			Value: []byte(namespace),
		},
		{
			Key:   "name",
			Value: []byte(name),
		},
		{
			Key:   "status",
			Value: statusBytes,
		},
		{
			Key:   "comment",
			Value: []byte(comment),
		},
	}

	resp, err := m.Invoke(SET_FN_IMPL_BY_NAME_METHOD_NAME, params, "")
	if err != nil {
		return err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		return nil
	} else {
		return fmt.Errorf("set function implement error, code: %d, msg: %s", resp.Code, resp.ContractResult.Message)
	}
}
