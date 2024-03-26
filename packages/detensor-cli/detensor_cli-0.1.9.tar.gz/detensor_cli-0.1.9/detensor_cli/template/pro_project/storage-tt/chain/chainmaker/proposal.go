package chainmaker

import (
	"encoding/binary"
	"encoding/json"
	"fmt"

	"chainmaker.org/chainmaker/pb-go/v2/common"
)

const (
	CREATE_PROPOSAL_METHOD_NAME         = "create_proposal"
	REVOKE_PROPOSAL_METHOD_NAME         = "revoke_proposal"
	REVOKE_PROPOSAL_BY_NAME_METHOD_NAME = "revoke_proposal_by_name"
	PERMIT_PROPOSAL_METHOD_NAME         = "permit_proposal"
	PERMIT_PROPOSAL_BY_NAME_METHOD_NAME = "permit_proposal_by_name"
	COMMIT_PROPOSAL_METHOD_NAME         = "commit_proposal"
	COMMIT_PROPOSAL_BY_NAME_METHOD_NAME = "commit_proposal_by_name"

	CREATE_GLOBAL_PROPOSAL_METHOD_NAME         = "create_global_proposal"
	REVOKE_GLOBAL_PROPOSAL_METHOD_NAME         = "revoke_global_proposal"
	REVOKE_GLOBAL_PROPOSAL_BY_NAME_METHOD_NAME = "revoke_global_proposal_by_name"
	PERMIT_GLOBAL_PROPOSAL_METHOD_NAME         = "permit_global_proposal"
	PERMIT_GLOBAL_PROPOSAL_BY_NAME_METHOD_NAME = "permit_global_proposal_by_name"
	COMMIT_GLOBAL_PROPOSAL_METHOD_NAME         = "commit_global_proposal"
	COMMIT_GLOBAL_PROPOSAL_BY_NAME_METHOD_NAME = "commit_global_proposal_by_name"
)

func (m *ChainMakerModel) CreateProposal(proposal json.RawMessage, namespace string) (uint64, error) {
	params := []*common.KeyValuePair{
		{
			Key:   "object",
			Value: proposal,
		},
		{
			Key:   "namespace",
			Value: []byte(namespace),
		},
	}

	resp, err := m.Invoke(CREATE_PROPOSAL_METHOD_NAME, params, "")
	if err != nil {
		return 0, err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		res := resp.ContractResult.Result
		ret := binary.BigEndian.Uint64(res)
		return ret, nil
	} else {
		return 0, fmt.Errorf("create proposal error, code: %d, msg: %s", resp.Code, resp.ContractResult.Message)
	}
}

func (m *ChainMakerModel) RevokeProposal(uid uint64) error {
	uidBytes := make([]byte, 8)
	binary.BigEndian.PutUint64(uidBytes, uid)
	params := []*common.KeyValuePair{
		{
			Key:   "uid",
			Value: uidBytes,
		},
	}
	resp, err := m.Invoke(REVOKE_PROPOSAL_METHOD_NAME, params, "")
	if err != nil {
		return err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		return nil
	} else {
		return fmt.Errorf("revoke proposal error, code: %d, msg: %s", resp.Code, resp.ContractResult.Message)
	}
}

func (m *ChainMakerModel) RevokeProposalByName(namespace, name string) error {
	params := []*common.KeyValuePair{
		{
			Key:   "namespace",
			Value: []byte(namespace),
		},
		{
			Key:   "name",
			Value: []byte(name),
		},
	}

	resp, err := m.Invoke(REVOKE_PROPOSAL_BY_NAME_METHOD_NAME, params, "")
	if err != nil {
		return err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		return nil
	} else {
		return fmt.Errorf("revoke globalproposal error, code: %d, msg: %s", resp.Code, resp.ContractResult.Message)
	}
}

func (m *ChainMakerModel) CommitProposal(uid uint64) ([]json.RawMessage, error) {
	uidBytes := make([]byte, 8)
	binary.BigEndian.PutUint64(uidBytes, uid)
	params := []*common.KeyValuePair{
		{
			Key:   "uid",
			Value: uidBytes,
		},
	}

	resp, err := m.Invoke(COMMIT_PROPOSAL_METHOD_NAME, params, "")
	if err != nil {
		return nil, err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		ret := resp.ContractResult.Result
		array := []json.RawMessage{}
		err = json.Unmarshal(ret, &array)
		return array, err
	} else {
		return nil, fmt.Errorf("commit proposal error, code: %d, msg: %s", resp.Code, resp.ContractResult.Message)
	}
}

func (m *ChainMakerModel) CommitProposalByName(namespace, name string) ([]json.RawMessage, error) {
	params := []*common.KeyValuePair{
		{
			Key:   "namespace",
			Value: []byte(namespace),
		},
		{
			Key:   "name",
			Value: []byte(name),
		},
	}

	resp, err := m.Invoke(COMMIT_PROPOSAL_BY_NAME_METHOD_NAME, params, "")
	if err != nil {
		return nil, err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		ret := resp.ContractResult.Result
		array := []json.RawMessage{}
		err = json.Unmarshal(ret, &array)
		return array, err
	} else {
		return nil, fmt.Errorf("commit proposal error, code: %d, msg: %s", resp.Code, resp.ContractResult.Message)
	}
}

func (m *ChainMakerModel) PermitProposal(uid uint64, status bool, comment string) (bool, error) {
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

	resp, err := m.Invoke(PERMIT_PROPOSAL_METHOD_NAME, params, "")
	if err != nil {
		return false, err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		return false, nil
	} else {
		return false, fmt.Errorf("permit proposal error, code: %d, msg: %s", resp.Code, resp.ContractResult.Message)
	}
}

func (m *ChainMakerModel) PermitProposalByName(namespace, name string, status bool, comment string) (bool, error) {
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
			Value: EncodeBool(status),
		},
		{
			Key:   "comment",
			Value: []byte(comment),
		},
	}

	resp, err := m.Invoke(PERMIT_PROPOSAL_BY_NAME_METHOD_NAME, params, "")
	if err != nil {
		return false, err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		return false, nil
	} else {
		return false, fmt.Errorf("permit proposal by name error, code: %d, msg: %s",
			resp.Code, resp.ContractResult.Message)
	}
}

func (m *ChainMakerModel) CreateGlobalProposal(object json.RawMessage) (uint64, error) {
	params := []*common.KeyValuePair{
		{
			Key:   "object",
			Value: object,
		},
	}

	resp, err := m.Invoke(CREATE_GLOBAL_PROPOSAL_METHOD_NAME, params, "")
	if err != nil {
		return 0, err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		res := resp.ContractResult.Result
		ret := binary.BigEndian.Uint64(res)
		return ret, nil
	} else {
		return 0, fmt.Errorf("create globalproposal error, code: %d, msg: %s", resp.Code, resp.ContractResult.Message)
	}
}

func (m *ChainMakerModel) RevokeGlobalProposal(uid uint64) error {
	params := []*common.KeyValuePair{
		{
			Key:   "uid",
			Value: EncodeUint64(uid),
		},
	}
	resp, err := m.Invoke(REVOKE_GLOBAL_PROPOSAL_METHOD_NAME, params, "")
	if err != nil {
		return err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		return nil
	} else {
		return fmt.Errorf("revoke globalproposal error, code: %d, msg: %s", resp.Code, resp.ContractResult.Message)
	}
}

func (m *ChainMakerModel) RevokeGlobalProposalByName(name string) error {
	params := []*common.KeyValuePair{
		{
			Key:   "name",
			Value: []byte(name),
		},
	}
	resp, err := m.Invoke(REVOKE_GLOBAL_PROPOSAL_BY_NAME_METHOD_NAME, params, "")
	if err != nil {
		return err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		return nil
	} else {
		return fmt.Errorf("revoke globalproposal by name error, code: %d, msg: %s",
			resp.Code, resp.ContractResult.Message)
	}

}

func (m *ChainMakerModel) CommitGlobalProposal(uid uint64) ([]json.RawMessage, error) {
	params := []*common.KeyValuePair{
		{
			Key:   "uid",
			Value: EncodeUint64(uid),
		},
	}

	resp, err := m.Invoke(COMMIT_GLOBAL_PROPOSAL_METHOD_NAME, params, "")
	if err != nil {
		return nil, err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		ret := resp.ContractResult.Result
		array := []json.RawMessage{}
		err = json.Unmarshal(ret, &array)
		return array, err
	} else {
		return nil, fmt.Errorf("commit proposal error, code: %d, msg: %s", resp.Code, resp.ContractResult.Message)
	}
}

func (m *ChainMakerModel) CommitGlobalProposalByName(name string) ([]json.RawMessage, error) {
	params := []*common.KeyValuePair{
		{
			Key:   "name",
			Value: []byte(name),
		},
	}

	resp, err := m.Invoke(COMMIT_GLOBAL_PROPOSAL_BY_NAME_METHOD_NAME, params, "")
	if err != nil {
		return nil, err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		ret := resp.ContractResult.Result
		array := []json.RawMessage{}
		err = json.Unmarshal(ret, &array)
		return array, err
	} else {
		return nil, fmt.Errorf("commit proposal error, code: %d, msg: %s", resp.Code, resp.ContractResult.Message)
	}

}

func (m *ChainMakerModel) PermitGlobalProposal(uid uint64, status bool, comment string) (bool, error) {
	params := []*common.KeyValuePair{
		{
			Key:   "uid",
			Value: EncodeUint64(uid),
		},
		{
			Key:   "status",
			Value: EncodeBool(status),
		},
		{
			Key:   "comment",
			Value: []byte(comment),
		},
	}

	resp, err := m.Invoke(PERMIT_GLOBAL_PROPOSAL_METHOD_NAME, params, "")
	if err != nil {
		return false, err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		return false, nil
	} else {
		return false, fmt.Errorf("permit globalproposal error, code: %d, msg: %s", resp.Code, resp.ContractResult.Message)
	}
}

func (m *ChainMakerModel) PermitGlobalProposalByName(name string, status bool, comment string) (bool, error) {
	params := []*common.KeyValuePair{
		{
			Key:   "name",
			Value: []byte(name),
		},
		{
			Key:   "status",
			Value: EncodeBool(status),
		},
		{
			Key:   "comment",
			Value: []byte(comment),
		},
	}

	resp, err := m.Invoke(PERMIT_GLOBAL_PROPOSAL_BY_NAME_METHOD_NAME, params, "")
	if err != nil {
		return false, err
	}

	if resp.Code == common.TxStatusCode_SUCCESS {
		return false, nil
	} else {
		return false, fmt.Errorf("permit globalproposal by name error, code: %d, msg: %s", resp.Code, resp.ContractResult.Message)
	}
}
