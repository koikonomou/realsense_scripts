#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API

#include <fstream>              // File IO
#include <iostream>             // Terminal IO
#include <sstream>              // Stringstreams
#include <iomanip>
#include <string>
#include <thread>

// 3rd party header for writing png files
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

// Helper function for writing metadata to disk as a csv file
void metadata_to_csv(const rs2::frame& frm, const std::string& filename);
void print_info(rs2::device& dev);
// This sample captures 30 frames and writes the last frame to disk.
// It can be useful for debugging an embedded system with no display.
int main(int argc, char * argv[]) try
{   
    rs2::device dev=[] {
        rs2::context ctx;
        std::cout << "Waiting for device..." << std::endl;
        while(true){
            for(auto&& dev : ctx.query_devices())
                return dev;
            // std::this_tread::sleep_for(std::chrono::milliseconds(10));
        }
    }();
    print_info(dev);

    // Declare depth colorizer for pretty visualization of depth data
    rs2::colorizer color_map;

    // Declare RealSense pipeline, encapsulating the actual device and sensors
    rs2::pipeline p;
    rs2::config cfg;
    // std::string serial_number = dev.get_info()
    std::string serial_number = dev.get_info(RS2_CAMERA_INFO_SERIAL_NUMBER);
    cfg.enable_device(serial_number);
    std::cout << "Opening pipeline for serial_number: " << serial_number  << std::endl;
    // Start streaming with default recommended configuration
    p.start(cfg);

    // Capture 30 frames to give autoexposure, etc. a chance to settle
    for (auto i = 0; i < 30; ++i) p.wait_for_frames();

    // Wait for the next set of frames from the camera. Now that autoexposure, etc.
    // has settled, we will write these to disk
    for (auto&& frame : p.wait_for_frames())
    {
        // We can only save video frames as pngs, so we skip the rest
        if (auto vf = frame.as<rs2::video_frame>())
        {
            auto stream = frame.get_profile().stream_type();
            // Use the colorizer to get an rgb image for the depth stream
            if (vf.is<rs2::depth_frame>()) vf = color_map.process(frame);


            // Write images to disk
            std::stringstream png_file;
            png_file << "rs-save-to-disk-output-" << vf.get_profile().stream_name() << ".png";
            stbi_write_png(png_file.str().c_str(), vf.get_width(), vf.get_height(),
                           vf.get_bytes_per_pixel(), vf.get_data(), vf.get_stride_in_bytes());
            std::cout << "Saved " << png_file.str() << std::endl;

            // Record per-frame metadata for UVC streams
            std::stringstream csv_file;
            csv_file << "rs-save-to-disk-output-" << vf.get_profile().stream_name()
                     << "-metadata.csv";
            metadata_to_csv(vf, csv_file.str());
        }
    }

    return EXIT_SUCCESS;
}
catch(const rs2::error & e)
{
    std::cerr << "RealSense error calling " << e.get_failed_function() << "(" << e.get_failed_args() << "):\n    " << e.what() << std::endl;
    return EXIT_FAILURE;
}
catch(const std::exception & e)
{
    std::cerr << e.what() << std::endl;
    return EXIT_FAILURE;
}

void metadata_to_csv(const rs2::frame& frm, const std::string& filename)
{
    std::ofstream csv;

    csv.open(filename);

    //    std::cout << "Writing metadata to " << filename << endl;
    csv << "Stream," << rs2_stream_to_string(frm.get_profile().stream_type()) << "\nMetadata Attribute,Value\n";

    // Record all the available metadata attributes
    for (size_t i = 0; i < RS2_FRAME_METADATA_COUNT; i++)
    {
        if (frm.supports_frame_metadata((rs2_frame_metadata_value)i))
        {
            csv << rs2_frame_metadata_to_string((rs2_frame_metadata_value)i) << ","
                << frm.get_frame_metadata((rs2_frame_metadata_value)i) << "\n";
        }
    }

    csv.close();
}

void print_info(rs2::device& dev) {
    std::cout << "device found:" << std::endl;
    std::cout << dev.get_info(RS2_CAMERA_INFO_NAME) << " "
              << dev.get_info(RS2_CAMERA_INFO_SERIAL_NUMBER) << " "
              << dev.get_info(RS2_CAMERA_INFO_PRODUCT_ID) << std::endl;

    auto sensors = dev.query_sensors();
    for (rs2::sensor& sensor : sensors) {
        std::cout << "sensor " << sensor.get_info(RS2_CAMERA_INFO_NAME) << std::endl;
        for (rs2::stream_profile& profile : sensor.get_stream_profiles()) {
            std::cout << "  stream " << profile.stream_name() << std::endl;
        }
    }
}