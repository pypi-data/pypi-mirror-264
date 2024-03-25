package test

import (
	"fmt"
	"net/http"
	"testing"
)

func TestCreateDeclare(t *testing.T) {
	cluster.ReInit()
	nsProposal := ReadTestData(t, "declare", "create-namespace-proposal.json")
	resp, err := cluster.PostRawJson(0, "/api/core/v1/globalproposal/", nsProposal, nil)
	RequireHttpResp(t, "create-ns-proposal", resp, err, http.StatusCreated)

	for i := 0; i < 3; i++ {
		resp, err = cluster.PutPlainText(
			i,
			"/api/core/v1/globalproposal/ns-proposal/permission",
			fmt.Sprintf("comment from org %d", i+1),
			nil,
		)
		RequireHttpResp(t, "permit-ns-proposal", resp, err, http.StatusOK)
	}
	resp, err = cluster.PutJson(
		0, "/api/core/v1/globalproposal/ns-proposal/commit",
		nil, nil,
	)
	RequireHttpResp(t, "commit-ns-proposal", resp, err, http.StatusOK)

	dataDeclareProposal := ReadTestData(t, "declare", "create-data-declare.json")
	resp, err = cluster.PostRawJson(0, "/api/core/v1/namespace/example-ns/proposal", dataDeclareProposal, nil)
	RequireHttpResp(t, "create declare proposal", resp, err, http.StatusCreated)

	resp, err = cluster.Get(0, "/api/core/v1/namespace/example-ns/proposal/create-data-declare-proposal", nil)
	out := RequireHttpResp(t, "get declare proposal", resp, err, http.StatusOK)
	t.Logf("get proposal: %s", string(out))

	for i := 0; i < 3; i++ {
		resp, err = cluster.PutPlainText(
			i,
			"/api/core/v1/namespace/example-ns/proposal/create-data-declare-proposal/permission",
			fmt.Sprintf("comment from org %d", i+1),
			nil,
		)
		RequireHttpResp(t, "permit-ns-proposal", resp, err, http.StatusOK)
	}
	resp, err = cluster.PutJson(
		0, "/api/core/v1/namespace/example-ns/proposal/create-data-declare-proposal/commit",
		nil, nil,
	)
	RequireHttpResp(t, "commit-declare-proposal", resp, err, http.StatusOK)

	resp, err = cluster.Get(
		0, "/api/core/v1/namespace/example-ns/datadeclare/example-data-declare",
		nil,
	)

	out = RequireHttpResp(t, "get-data-declare", resp, err, http.StatusOK)
	t.Logf("created data declare: %s", out)
}

func TestImplementDeclare(t *testing.T) {
	// cluster.ReInit()
}

func TestDeleteDeclare(t *testing.T) {
	// cluster.ReInit()

}
