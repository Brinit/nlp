#include "tensorflow/core/public/session.h"
#include "tensorflow/core/public/env.h"
#include "loader.h"

using namespace tensorflow;

std::string f(int aval, int bval) {
  // Initialize a tensorflow session
  Session* session;
  Status status = NewSession(SessionOptions(), &session);
  if (!status.ok()) {
    std::cout << status.ToString() << "\n";
    return "error "+status.ToString();;
  }

  // Read in the protobuf graph we exported
  // (The path seems to be relative to the cwd. Keep this in mind
  // when using `bazel run` since the cwd isn't where you call
  // `bazel run` but from inside a temp folder.)
  GraphDef graph_def;
  status = ReadBinaryProto(Env::Default(), "models/train.pb", &graph_def);
  if (!status.ok()) {
    std::cout << status.ToString() << "\n";
    return "error "+status.ToString();;
  }

  // Add the graph to the session
  status = session->Create(graph_def);
  if (!status.ok()) {
    std::cout << status.ToString() << "\n";
    return "error "+status.ToString();;
  }

  // Setup inputs and outputs:

  // Our graph doesn't require any inputs, since it specifies default values,
  // but we'll change an input to demonstrate.
  Tensor a(DT_FLOAT, TensorShape());
  a.scalar<float>()() = aval;

  Tensor b(DT_FLOAT, TensorShape());
  b.scalar<float>()() = bval;

  std::vector<std::pair<string, tensorflow::Tensor>> inputs = {
    { "a", a },
    { "b", b },
  };

  // The session will initialize the outputs
  std::vector<tensorflow::Tensor> outputs;

  // Run the session, evaluating our "c" operation from the graph
  status = session->Run(inputs, {"c"}, {}, &outputs);
  if (!status.ok()) {
    std::cout << status.ToString() << "\n";
    return "error "+status.ToString();
  }

  // Grab the first output (we only evaluated one graph node: "c")
  // and convert the node to a scalar representation.
  auto output_c = outputs[0].scalar<float>();

  // (There are similar methods for vectors and matrices here:
  // https://github.com/tensorflow/tensorflow/blob/master/tensorflow/core/public/tensor.h)

  // Print the results
  std::cout << outputs[0].DebugString() << "\n"; // Tensor<type: float shape: [] values: 30>
  std::cout << output_c() << "\n"; // 30

  // Free any resources used by the session
  session->Close();
  return outputs[0].DebugString();
}