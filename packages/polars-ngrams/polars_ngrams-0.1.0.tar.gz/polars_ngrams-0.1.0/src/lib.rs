mod expressions;

use mimalloc::MiMalloc;

#[global_allocator]
static GLOBAL: MiMalloc = MiMalloc;

use pyo3::types::PyModule;
use pyo3::{pymodule, PyResult, Python};

#[pymodule]
fn polars_ngrams(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}