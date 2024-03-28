use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use image::{DynamicImage, imageops};
use std::convert::TryInto;
use std::io::Cursor;
use image::GenericImage;
use async_std::task;
use image::GenericImageView;

#[pyfunction]
fn create_chart(_py: Python, image_bytes_list: Vec<Vec<u8>>) -> PyResult<Vec<u8>> {
    let result: Result<Vec<u8>, PyErr> = task::block_on(async {
        let rows = (image_bytes_list.len() as f32).sqrt().ceil() as u32;
        let cols = (image_bytes_list.len() as f32 / rows as f32).ceil() as u32;

        let mut result_image = DynamicImage::new_rgba8(cols * 256, rows * 256);

        let mut x = 0;
        let mut y = 0;
        for image_bytes in image_bytes_list {
            let img = image::load_from_memory(&image_bytes)
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Error loading image: {}", e)))?;

            let resized_img = img.resize(256, 256, imageops::FilterType::Lanczos3);
            let (width, height) = resized_img.dimensions();
            // println!("Resized image dimensions: {} x {}", width, height);

            result_image.copy_from(&resized_img.to_rgba8(), x * 256, y * 256)
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Error pasting image: {}", e)))?;

            x += 1;
            if x == cols {
                x = 0;
                y += 1;
            }
        }

        let mut buffer = Cursor::new(Vec::new());
        result_image.write_to(&mut buffer, image::ImageOutputFormat::Png)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Error writing image to buffer: {}", e)))?;

        Ok(buffer.into_inner())
    });
    match result {
        Ok(hex) => Ok(hex),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{}", e))),
    }
    
}

#[pymodule]
fn rust_chart_generator(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(create_chart, m)?)?;
    Ok(())
}
