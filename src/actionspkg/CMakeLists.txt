cmake_minimum_required(VERSION 3.0.2)
project(actionspkg)

find_package(catkin REQUIRED COMPONENTS
  actionlib
  actionlib_msgs
  message_generation
  roscpp
  std_msgs
)

find_package(Boost REQUIRED COMPONENTS system)

add_action_files(
  FILES
  Fibonacci.action
)

generate_messages(
  DEPENDENCIES
  actionlib_msgs
  std_msgs
)


catkin_package(
 INCLUDE_DIRS include
 LIBRARIES actionspkg
 CATKIN_DEPENDS actionlib actionlib_msgs message_generation roscpp std_msgs
 DEPENDS system_lib
)

include_directories(
  ${catkin_INCLUDE_DIRS}
  ${Boost_INCLUDE_DIRS}
)

add_executable(action_server src/action_server.cpp)
add_dependencies(action_server ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(action_server ${catkin_LIBRARIES})
add_executable(action_client src/action_client.cpp)
add_dependencies(action_client ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(action_client ${catkin_LIBRARIES})