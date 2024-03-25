use contract::objects::core::v1::{
    Contract, DataDeclare, FunctionDeclare, GlobalProposal, Namespace, Proposal,
};

fn main() {
    let mut gen = schemars::gen::SchemaSettings::openapi3()
        .with(|s| {
            s.option_add_null_type = true;
            s.option_nullable = true;
        })
        .into_generator();

    gen.subschema_for::<DataDeclare>();
    gen.subschema_for::<FunctionDeclare>();
    gen.subschema_for::<Contract>();
    gen.subschema_for::<GlobalProposal>();
    gen.subschema_for::<Proposal>();
    let schema = gen.into_root_schema_for::<Namespace>();
    println!("{}", serde_json::to_string_pretty(&schema).unwrap());
}
