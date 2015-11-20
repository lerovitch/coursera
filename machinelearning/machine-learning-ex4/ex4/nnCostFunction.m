function [J grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, ...
                                   X, y, lambda)
%NNCOSTFUNCTION Implements the neural network cost function for a two layer
%neural network which performs classification
%   [J grad] = NNCOSTFUNCTON(nn_params, hidden_layer_size, num_labels, ...
%   X, y, lambda) computes the cost and gradient of the neural network. The
%   parameters for the neural network are "unrolled" into the vector
%   nn_params and need to be converted back into the weight matrices.
%
%   The returned parameter grad should be a "unrolled" vector of the
%   partial derivatives of the neural network.
%

% Reshape nn_params back into the parameters Theta1 and Theta2, the weight matrices
% for our 2 layer neural network
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

% Setup some useful variables
m = size(X, 1);  % 5000 training sets

% You need to return the following variables correctly
J = 0;
Theta1_grad = zeros(size(Theta1));
Theta2_grad = zeros(size(Theta2));

% ====================== YOUR CODE HERE ======================
% Instructions: You should complete the code by working through the
%               following parts.
%
% Part 1: Feedforward the neural network and return the cost in the
%         variable J. After implementing Part 1, you can verify that your
%         cost function computation is correct by verifying the cost
%         computed in ex4.m

a1 = [ones(m, 1) X]; % add ones to data matrix 5000 x 401
z2 = Theta1 * a1';
a2 = [ones(m,1) sigmoid(z2)']; % 5000 x 26
z3 = Theta2 * a2';
a3 = sigmoid(z3)'; % 5000 x 10

rng = 1:num_labels;
cmp = repmat(rng, m, 1);
y_res = cmp == y;  % 5000 x 10

% point to point multiplication with .* between y and a2
partial_k = (-y_res .* (log(a3))) - ((1 - y_res) .* log(1 - a3));  % 5000 x 10
J = 1 / m * sum(sum(partial_k));

Theta1_r = Theta1;
Theta2_r = Theta2;
Theta1_r(:, 1) = [];
Theta2_r(:, 1) = [];
Theta1_reg = sum(sum((Theta1_r .* Theta1_r)));
Theta2_reg = sum(sum((Theta2_r .* Theta2_r)));
reg = (lambda / (2 * m)) * (Theta1_reg + Theta2_reg);

J = J + reg;

% Part 2: Implement the backpropagation algorithm to compute the gradients
%         Theta1_grad and Theta2_grad. You should return the partial derivatives of
%         the cost function with respect to Theta1 and Theta2 in Theta1_grad and
%         Theta2_grad, respectively. After implementing Part 2, you can check
%         that your implementation is correct by running checkNNGradients
%
%         Note: The vector y passed into the function is a vector of labels
%               containing values from 1..K. You need to map this vector into a
%               binary vector of 1's and 0's to be used with the neural network
%               cost function.
%
%         Hint: We recommend implementing backpropagation using a for-loop
%               over the training examples if you are implementing it for the
%               first time.
%
delta_3 = a3 - y_res;  % 5000 x 10
delta_2 = ((Theta2' * delta_3') .* (a2 - (a2 .* a2))')';    % (26x10) x (10 x 5000) = (26x5000)'
delta_2(:, 1) = [];

D1 = ((1 / m) * (a1' * delta_2))';  % (401 x 5000) x (5000 x 25)
D2 = ((1 / m) * (a2' * delta_3))';  % (25 x 5000) x (5000 x 10)



% Part 3: Implement regularization with the cost function and gradients.
%
%         Hint: You can implement this around the code for
%               backpropagation. That is, you can compute the gradients for
%               the regularization separately and then add them to Theta1_grad
%               and Theta2_grad from Part 2.
%


Theta1_grad = D1 + (lambda / m) * Theta1;
Theta1_grad(:, 1) = D1(:, 1)
Theta2_grad = D2 + (lambda / m) * Theta2;
Theta2_grad(:, 1) = D2(:, 1)
















% -------------------------------------------------------------

% =========================================================================

% Unroll gradients
grad = [Theta1_grad(:) ; Theta2_grad(:)];


end
