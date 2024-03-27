use crate::chainmaker_sdk::sim_context::{result_code, SUCCESS_CODE};

#[macro_export]
macro_rules! contract_call {
    ($call:ident, $f:expr) => {
        #[no_mangle]
        pub extern "C" fn $call() {
            let ctx = &mut $crate::chainmaker_sdk::sim_context::get_sim_context();
            match $f(ctx) {
                Ok(v) => {
                    ctx.ok(&v);
                }
                Err(err) => {
                    ctx.error(&format!("{}", err));
                }
            }
        }
    };
}

#[macro_export]
macro_rules! contract_call_no_ret {
    ($call:ident, $f:expr) => {
        #[no_mangle]
        pub extern "C" fn $call() {
            let ctx = &mut $crate::chainmaker_sdk::sim_context::get_sim_context();
            match $f(ctx) {
                Ok(_) => {
                    ctx.ok("ok".as_bytes());
                }
                Err(err) => {
                    ctx.error(&format!("{}", err));
                }
            };
        }
    };
}

#[derive(Debug)]
pub struct SysCallError(&'static str, result_code);

impl std::fmt::Display for SysCallError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_fmt(format_args!("syscall: {}, result_code: {}", self.0, self.1))
    }
}

impl std::error::Error for SysCallError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        None
    }

    fn description(&self) -> &str {
        "description() is deprecated; use Display"
    }

    fn cause(&self) -> Option<&dyn std::error::Error> {
        self.source()
    }
}

pub fn sys_call_err(call: &'static str) -> impl Fn(result_code) -> SysCallError {
    move |code| SysCallError(call, code)
}

pub fn sys_call(call: &'static str, code: result_code) -> Result<(), SysCallError> {
    if code == SUCCESS_CODE {
        Ok(())
    } else {
        Err(SysCallError(call, code))
    }
}
