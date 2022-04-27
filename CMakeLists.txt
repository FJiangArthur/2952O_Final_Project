cmake_minimum_required(VERSION 3.5)
project(see-pick-mirobot)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
add_compile_options(-g)

## is used, also find other catkin packages
if(POLICY CMP0057)
    cmake_policy(SET CMP0057 NEW)
endif()

set(_opencv_version 4)
find_package(OpenCV 4 QUIET COMPONENTS imgproc highgui)
if(NOT OpenCV_FOUND)
  message(STATUS "----------------Did not find OpenCV 4, trying OpenCV 3--------------")
  set(_opencv_version 3)
  find_package(OpenCV 3 REQUIRED COMPONENTS imgproc highgui)
endif()
find_package(depthai CONFIG REQUIRED)
# find_package(depthai CONFIG REQUIRED PATHS "/home/sachin/Desktop/luxonis/depthai-core/build/install/lib/cmake/depthai")

set(mobilenet_blob "${PROJECT_SOURCE_DIR}/resources/mobilenet-ssd_openvino_2021.2_6shave.blob")
file(DOWNLOAD "https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/mobilenet-ssd_openvino_2021.2_6shave.blob"
${mobilenet_blob}
TIMEOUT 60  # seconds
EXPECTED_HASH SHA1=f0e14978b3f77a4f93b9f969cd39e58bb7aef490
TLS_VERIFY ON)

set(tiny_yolo_v4_blob "${PROJECT_SOURCE_DIR}/resources/tiny-yolo-v4_openvino_2021.2_6shave.blob")
file(DOWNLOAD "https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/tiny-yolo-v4_openvino_2021.2_6shave.blob"
  ${tiny_yolo_v4_blob}
  TIMEOUT 60  # seconds
  EXPECTED_HASH SHA1=219d949610a5760e62a8458941e1300b81c3fe4a
  TLS_VERIFY ON)

find_package(ament_cmake QUIET)


if( CATKIN_DEVEL_PREFIX OR CATKIN_BUILD_BINARY_PACKAGE )
  find_package(catkin REQUIRED COMPONENTS
    camera_info_manager
    depthai_ros_msgs
    roscpp
    sensor_msgs
    std_msgs
    cv_bridge
    vision_msgs
    depthai_bridge
    message_filters
    nodelet
  )

  catkin_package(
    # INCLUDE_DIRS include
    LIBRARIES ${PROJECT_NAME}
    CATKIN_DEPENDS depthai_ros_msgs roscpp sensor_msgs std_msgs camera_info_manager depthai_bridge vision_msgs cv_bridge message_filters
    DEPENDS
    OpenCV
  )

  macro(mirobot_add_node node_name node_src)
      add_executable("${node_name}" "${node_src}")

      add_dependencies("${node_name}"
        ${catkin_EXPORTED_TARGETS}
        ${${PROJECT_NAME}_EXPORTED_TARGETS}
      )

      target_link_libraries("${node_name}"
        ${catkin_LIBRARIES}
        depthai::core
        opencv_imgproc
        opencv_highgui
      )

  endmacro()

  ## Specify additional locations of header files
  ## Your package locations should be listed before other locations
  include_directories(
    include
    ${catkin_INCLUDE_DIRS}
    ${OpenCV_INCLUDE_DIRS}
  )

#2952O Commented out
#   add_library(nodelet_stereo ros1_src/stereo_nodelet.cpp)

  add_dependencies(nodelet_stereo ${${PROJECT_NAME}_EXPORTED_TARGETS}
    ${catkin_EXPORTED_TARGETS}
  )

#2952O Commented out
#   target_link_libraries(nodelet_stereo
#     ${catkin_LIBRARIES}
#     depthai::core
#     opencv_imgproc
#     opencv_highgui
#   )

#2952O Commented out
    mirobot_add_node(rgb_listener src/rgb_listener.py)
#   mirobot_add_node(crop_control_service ros1_src/crop_control_service.cpp)
#   mirobot_add_node(mobilenet_node ros1_src/mobilenet_publisher.cpp)
#   mirobot_add_node(rgb_node ros1_src/rgb_publisher.cpp)
#   mirobot_add_node(rgb_stereo_node ros1_src/rgb_stereo_node.cpp)
#   mirobot_add_node(rgb_subscriber_node ros1_src/rgb_video_subscriber.cpp)
#   # mirobot_add_node(stereo_mimic_node ros1_src/stereo_mimic_node.cpp)
#   mirobot_add_node(stereo_inertial_node ros1_src/stereo_inertial_publisher.cpp)
#
#   mirobot_add_node(stereo_node ros1_src/stereo_publisher.cpp)
#   mirobot_add_node(yolov4_spatial_node ros1_src/yolov4_spatial_publisher.cpp)

#2952O Commented out
#   target_compile_definitions(mobilenet_node PRIVATE BLOB_PATH="${mobilenet_blob}")
#   target_compile_definitions(yolov4_spatial_node PRIVATE BLOB_PATH="${tiny_yolo_v4_blob}")


  ## Install these nodes
  install(TARGETS
            rgb_listener
#           crop_control_service
#           mobilenet_node
#           rgb_node
#           rgb_stereo_node
#           rgb_subscriber_node
#           # stereo_mimic_node
#           stereo_inertial_node
#           stereo_node
#           yolov4_spatial_node
          RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  )

  install(DIRECTORY launch/
	DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
	PATTERN ".svn" EXCLUDE
  )


endif()
