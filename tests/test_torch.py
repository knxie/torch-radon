import torch
import numpy as np
from torch.autograd import gradcheck
from torch_radon import Radon
from unittest import TestCase
from .utils import generate_random_images


class TestTorch(TestCase):
    def test_differentiation(self):
        device = torch.device('cuda')
        x = torch.FloatTensor(1, 64, 64).to(device)
        x.requires_grad = True
        angles = torch.FloatTensor(np.linspace(0, 2 * np.pi, 10).astype(np.float32)).to(device)

        radon = Radon(64, device)

        # check that backward is implemented for fp and bp
        y = radon.forward(x, angles)
        z = torch.mean(radon.backprojection(y, angles))
        z.backward()
        self.assertIsNotNone(x.grad)

    def test_shapes(self):
        """
        Check using channels is ok
        """
        device = torch.device('cuda')
        x = torch.FloatTensor(2, 3, 64, 64).to(device)
        angles = torch.FloatTensor(np.linspace(0, 2 * np.pi, 10).astype(np.float32)).to(device)
        radon = Radon(64, device)

        y = radon.forward(x, angles)
        self.assertEqual(y.size(), (2, 3, 10, 64))
        z = radon.backprojection(y, angles)
        self.assertEqual(z.size(), (2, 3, 64, 64))


#     def test_gradients(self):
#         device = torch.device('cuda')
#         radon = Radon(64).to(device)
#         x = torch.FloatTensor(generate_random_images(1, 64)).to(device)
#         x.requires_grad = True
#         angles = torch.FloatTensor(np.linspace(0, 2 * np.pi, 10).astype(np.float32)).to(device)

#         def f(xx):
#             return radon.backprojection(radon.forward(xx, angles), angles)
        
#         self.assertEqual(gradcheck(f, x, 1e-1, 1e-3, 1e-2), True)