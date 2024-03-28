#![allow(clippy::unused_unit)]
use polars::chunked_array::builder::AnonymousListBuilder;
use polars::prelude::*;
use pyo3_polars::derive::polars_expr;

#[derive(serde::Deserialize)]
struct Kwargs {
    pub n: usize,
}

fn output_type(fields: &[Field], kwargs: Kwargs) -> PolarsResult<Field> {
  let field_name = fields[0].name();
  
  Ok(Field::new(field_name, DataType::Array(Box::new(DataType::String), kwargs.n)))
}

#[polars_expr(output_type_func_with_kwargs=output_type)]
fn ngrams(inputs: &[Series], kwargs: Kwargs) -> PolarsResult<Series> {
    let series = inputs[0].list()?;

    let n = kwargs.n;

    let array_dtype = DataType::Array(Box::new(DataType::String), n);

    let out = series.apply_amortized(|s| {
        let series: &Series = s.as_ref();
        let row_strings = series.str().unwrap().into_iter().collect::<Vec<Option<&str>>>();

        let window_iter = row_strings.windows(n);
        let window_array_series = window_iter
            .map(|window| ChunkedArray::<StringType>::from_slice_options("", window).into_series())
            .collect::<Vec<_>>();

        let mut row_list_builder =
            AnonymousListBuilder::new("", n, array_dtype.inner_dtype().cloned());

        for window in window_array_series.iter() {
            // Error handling?
            let _ = row_list_builder.append_series(window);
        }

        row_list_builder.finish().into_series()
    });

    Ok(out.into_series())
}
