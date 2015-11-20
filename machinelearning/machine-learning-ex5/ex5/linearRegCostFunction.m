function [J, grad] = linearRegCostFunction(X, y, theta, lambda)
%LINEARREGCOSTFUNCTION Compute cost and gradient for regularized linear
%regression with multiple variables
%   [J, grad] = LINEARREGCOSTFUNCTION(X, y, theta, lambda) computes the
%   cost of using theta as the parameter for linear regression to fit the
%   data points in X and y. Returns the cost in J and the gradient in grad

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly
partial = X*theta - y;
reg_theta = theta;
reg_theta(1, :) = [];
J = (1 / (2*m)) * (partial'*partial);
J = J + (lambda / (2 * m))*(reg_theta' * reg_theta);
grad_c = (1 / m) * (partial)' * X;
grad = grad_c + (lambda / m) * theta';
grad(1) = grad_c(1);






% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost and gradient of regularized linear
%               regression for a particular choice of theta.
%
%               You should set J to the cost and grad to the gradient.
%












% =========================================================================

grad = grad(:);

end
