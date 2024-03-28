use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use async_std::task;
use image::GenericImageView;

#[pyfunction]
fn get_dominant_color(_py: Python, image_bytes: Vec<u8>) -> PyResult<String> {
    let result = task::block_on(async {
        let img = match image::load_from_memory(&image_bytes) {
            Ok(img) => img,
            Err(e) => return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("{}", e))),
        };
        
        let rgb = img.to_rgb8();
        let average_color = rgb.pixels().fold((0, 0, 0), |acc, px| (acc.0 + px.0[0] as u32, acc.1 + px.0[1] as u32, acc.2 + px.0[2] as u32));
        let num_pixels = rgb.width() * rgb.height();
        let avg_r = average_color.0 / num_pixels;
        let avg_g = average_color.1 / num_pixels;
        let avg_b = average_color.2 / num_pixels;
        Ok(format!("{:02X}{:02X}{:02X}", avg_r, avg_g, avg_b))
    });

    match result {
        Ok(hex) => Ok(hex),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{}", e))),
    }
}


#[pymodule]
fn colorgram_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_dominant_color, m)?)?;
    Ok(())
}
