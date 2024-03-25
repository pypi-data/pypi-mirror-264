package chainmaker

import (
	"encoding/binary"
	"encoding/json"
	"fmt"

	"chainmaker.org/chainmaker/pb-go/v2/common"
)

const (
	GET_OBJECT_BY_ID_METHOD_NAME   = "get_object_by_uid"
	GET_OBJECT_BY_KIND_METHOD_NAME = "get_object_by_kind"
	GET_OBJECT_BY_NAME_METHOD_NAME = "get_object_by_name"
)

func (m *ChainMakerModel) GetObjectByUid(uid uint64) (json.RawMessage, error) {
	uidBytes := make([]byte, 8)
	binary.BigEndian.PutUint64(uidBytes, uid)
	params := []*common.KeyValuePair{
		{
			Key:   "uid",
			Value: uidBytes,
		},
	}
	resp, err := m.Query(GET_OBJECT_BY_ID_METHOD_NAME, params)
	if err != nil {
		return nil, err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		ret := resp.ContractResult.Result
		return ret, nil
	} else {
		code := resp.Code
		msg := resp.GetMessage()
		return nil, fmt.Errorf("invoke %s failed, code: %d, msg: %s", GET_OBJECT_BY_ID_METHOD_NAME, code, msg)
	}
}

func (m *ChainMakerModel) GetObjectByName(apiVersion, kind, namespace, name, version string) (json.RawMessage, error) {
	params := []*common.KeyValuePair{
		{
			Key:   "apiVersion",
			Value: []byte(apiVersion),
		},
		{
			Key:   "kind",
			Value: []byte(kind),
		},
		{
			Key:   "namespace",
			Value: []byte(namespace),
		},
		{
			Key:   "name",
			Value: []byte(name),
		},
		{
			Key:   "version",
			Value: []byte(version),
		},
	}

	resp, err := m.client.QueryContract(m.contractName, GET_OBJECT_BY_NAME_METHOD_NAME, params, -1)
	if err != nil {
		return nil, err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		ret := resp.ContractResult.Result
		if len(ret) == 0 {
			ret = nil
		}
		return ret, nil
	} else {
		code := resp.Code
		msg := resp.GetMessage()
		return nil, fmt.Errorf("invoke %s failed, code: %d, msg: %s", GET_OBJECT_BY_NAME_METHOD_NAME, code, msg)
	}
}

func (m *ChainMakerModel) GetObjectByKind(apiVersion, kind, namespace string) ([]json.RawMessage, error) {
	params := []*common.KeyValuePair{
		{
			Key:   "apiVersion",
			Value: []byte(apiVersion),
		},
		{
			Key:   "kind",
			Value: []byte(kind),
		},
		{
			Key:   "namespace",
			Value: []byte(namespace),
		},
	}

	resp, err := m.Query(GET_OBJECT_BY_KIND_METHOD_NAME, params)
	if err != nil {
		return nil, err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		ret := resp.ContractResult.Result
		array := []json.RawMessage{}
		err = json.Unmarshal(ret, &array)
		return array, err
	} else {
		code := resp.Code
		msg := resp.GetMessage()
		return nil, fmt.Errorf("invoke %s failed, code: %d, msg: %s", GET_OBJECT_BY_KIND_METHOD_NAME, code, msg)
	}
}

func (m *ChainMakerModel) GetObjectWith(conds string) ([]json.RawMessage, error) {
	return nil, nil
}
