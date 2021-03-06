{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Darcy's Equation\n",
    "\n",
    "In this tutorial we will assume we have an incompressible fluid. Conservation of mass then gives us\n",
    "\\begin{equation}\n",
    "\\nabla v =  q,\n",
    "\\end{equation}\n",
    "where $v$ is the fluid velocity and $q$ any source term. \n",
    "\n",
    "A common assumption used for flow in porous media is the so called Darcy's law, which relates the flux field to the pressure gradient:\n",
    "\\begin{equation}\n",
    "v = -\\frac{K}{\\mu}\\nabla p\n",
    "\\end{equation}\n",
    "\n",
    "We innsert Darcy's law into the equation for conservation of mass to obtain an elliptic equation, which can be solved with respect to the pressure\n",
    "\n",
    "$$ - \\nabla \\cdot \\rho K \\nabla p = \\rho f $$\n",
    "with boundary conditions on $\\partial \\Omega_d$ and $\\partial \\Omega_n$:\n",
    "$$ p = p_b \\qquad - K \\nabla p \\cdot \\mathbf{n} = u_b$$\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Import modules\n",
    "To solve this equation in Porepy we import the Darcy module."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "\n",
    "from porepy.numerics import elliptic\n",
    "from porepy.fracs import meshing\n",
    "from porepy.params import bc, tensor, data\n",
    "from porepy.grids.grid import FaceTag\n",
    "from porepy.grids.structured import CartGrid\n",
    "from porepy.viz.plot_grid import plot_grid"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Generate grid\n",
    "We first solve the equation on a single cartesian grid, and will later add fractures to the grid"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "g = CartGrid([11, 11])\n",
    "g.compute_geometry()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Set parameters\n",
    "We create a parameter class and assign zero dirichlet boundary conditions, and a source term"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "param =  data.Parameters(g)\n",
    "dir_bound = np.ravel(np.argwhere((g.has_face_tag(FaceTag.BOUNDARY))))\n",
    "bc_cond = bc.BoundaryCondition(g, dir_bound, ['dir']*dir_bound.size)\n",
    "\n",
    "src = np.zeros(g.num_cells)\n",
    "src[60] = 1\n",
    "\n",
    "param.set_bc('flow', bc_cond)\n",
    "param.set_source('flow', src)\n",
    "d = {'param': param}"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Solve problem\n",
    "We can now create a Darcy object and solve the problem"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAVAAAADuCAYAAABvX19oAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz\nAAALEgAACxIB0t1+/AAAADl0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uIDIuMS4wLCBo\ndHRwOi8vbWF0cGxvdGxpYi5vcmcvpW3flQAAIABJREFUeJzt3Xl0VFW6+P3vTlVCIMQwJJCRqUEh\nKEIIBhC6EVGRblEwCggtMsgV8YpNt4qt0uBrO912bLztT1tx4EKut9dVuAgoojggESLYilHGBJIw\nSCJT5lTlef8oUh0iSepUqlIV8nzWOmtRVefsZ58qeNjnnD0YEUEppZR1IYGugFJKtVSaQJVSykua\nQJVSykuaQJVSykuaQJVSykuaQJVSykuaQJVSykuaQJVSykuaQJVSykt2i/vrsCWllKdMUw7ubYyU\nerjvYXhfRMY2JZ43rCZQpZRqFmXAPA/3fQii/VmX+uglfJBp3749+/fvP+dnr7/+OiNGjGjmGikV\nGAYI9XALlFaZQFesWEFqairt27cnLi6Oa6+9ls8//9zr8owx7N2796z3Tp8+zYIFC+jRowcRERF0\n69aN9PR0vvzyywbLKi4uplevXl7Vo7KyksWLF9OnTx8iIiLo0aMHM2fOJDc316vy/GXx4sVMmzYt\n0NXwq9zcXIwxOByOQFelxTK4LpE92QKl1SXQZ555hnvuuYc//vGPHD16lIMHD3LnnXeyatUqy2XV\n94+joqKC0aNH8+2337JmzRpOnTrF999/z+TJk1m3bp2lsqxIT09n9erVrFixgpMnT/LPf/6TwYMH\ns3HjxiaXrXxPk2vDWkILFBGxsrVoJ06ckIiICHn77bfr3efLL7+UoUOHSlRUlMTGxsq8efOkoqLC\n/TkgS5culd69e0uPHj1k5MiRAki7du0kIiJCMjIy5JVXXpHY2FgpLi5usD51y6p5b8+ePSIiUlhY\nKNddd51ERkbKkCFD5KGHHpLLL7/8nGVt2LBBwsPD5eDBg/XGKygokOuuu046duwov/jFL+Tll192\nf/anP/1J0tPTZerUqdK+fXu5+OKLZdeuXfLYY49JTEyMJCYmyvvvv+/e/1e/+pUsXLhQhgwZIpGR\nkTJ+/HgpKioSEZGPP/5YEhISzordvXt32bBhg6xbt05CQ0PFbrdLRESEDBgwQERcv83MmTMlNjZW\n4uPj5cEHHxSHw3HO8ygtLZVbb71VOnToIH379pUnn3zyrHgFBQUyceJEiY6Olh49esjzzz/v/qy8\nvFzmz58vcXFxEhcXJ/Pnz5fy8vKz6v3kk09KTEyMxMbGyjvvvCPvvfee9OnTRzp27Ch//vOf3WU5\nnU55/PHHpVevXtKpUye56aab3N9BUlKSABIRESERERHyxRdfyLJly2T48OFyzz33SKdOneSBBx6Q\njh07yjfffOMu8+jRo9K2bVv58ccf6/0dWxCr+eWsrTvIKx5uQFZT43mztaoEum7dOrHZbFJVVVXv\nPllZWbJlyxapqqqSnJwc6du3rzz77LPuzwEZM2aMFBUVSWlpqfu9mqQnIjJp0iSZPn16o/VprKxJ\nkybJTTfdJMXFxfLtt99KfHx8vQn0/vvvl1/+8pcNxhs5cqTMnTtXysrKZMeOHRIdHS0bN24UEVcC\nbdOmjaxfv16qqqrkt7/9rfTo0UMeffRRqayslJdfftmd5EVcCTQ+Pl6+/fZbKS4ulokTJ8rUqVNF\npOEEWhOrZt8aN9xwg8yZM0eKi4vl6NGjMmTIEHnppZcaPNeffvpJ8vLy5JJLLnHHczqdkpKSIkuW\nLJGKigrZt2+f9OzZU9avXy8iIg8//LCkpaXJ0aNH5ccff5Rhw4bJQw895K63zWaTJUuWuM85Ojpa\npkyZIqdOnZKdO3dKeHi47N+/X0REnnvuOUlLS5O8vDwpLy+XOXPmyOTJk0VEJCcnR4Cz/q4tW7ZM\nbDabvPDCC1JVVSWlpaUyd+5cue+++9z7PPfcc/Kb3/ymwd+xBWlScuoBsszDTRNoM1i+fLl07drV\n0jHPPvus3HDDDe7XgDvp1H6vdgK98sor5f7773e/3rFjh0RFRUlkZKRceOGFHpXlcDjEbrfL999/\n7/7sgQceqDeBzp49WyZNmlTveRw8eFBCQkLk1KlT7vcWLlzoTvR/+tOfZMyYMe7PVq9eLREREe5W\n4KlTpwSQ48ePi4grgdY+x++++05CQ0PF4XBYTqBHjhyRsLAw938iIiIrVqyQUaNGnfNcaidEEZFX\nXnnFHS8zM1OSkpLO2v+xxx6T2267TUREevXqJe+99577s/Xr10v37t1FxJVAw8PDf3bOmZmZ7v1T\nUlLknXfeERGRvn37yocffuj+7NChQ2K3293/+Z4rgdatW019q6urRURk8ODB8t///d/nPO8WqEnJ\nqSfIcg+3QCXQVtWNqXPnzhQWFuJwOLDbz33qu3fvZsGCBWRlZVFaWorD4WDw4MFn7ZOUlNRonMOH\nD7tfDxw4kBMnTvDhhx8ye/Zsj8o6duwYDofjrM+7d+/eYMzdu3fX+/mhQ4fo1KkTkZGRZ5WXlZXl\nft21a1f3n9u2bUt0dDQ2m839GlwPuTp06PCzunfv3p2qqioKCwvrrUN9Dhw4QFVVFXFxce73qqur\n6/1uDh06dNZntf984MABDh065K4jgNPpZOTIke5ja3+P3bt359ChQ+7XnTt3/tk51/1eiouL3bEm\nTJhASMi/HiXYbDaOHj1a77nWPae0tDTatWvHpk2biIuLY+/evYwfP77e41uTmodIwaxVPUQaNmwY\nbdq04d133613n7lz59K3b1/27NnDqVOneOyxx1xN9VqMabh/8JVXXskHH3xASUlJo3Wqr6yYmBjs\ndjt5eXnu9w4ePFhvOWPGjGHr1q3k5+ef8/P4+Hh++uknTp8+fVZ5CQkJjdaxPnXrFhoaSnR0NBER\nEZSW/qsLtNPp5NixY+7Xdc85KSmJNm3aUFhYyIkTJzhx4gSnTp3iu+++O2fcuLi4s86zdj2SkpLo\n2bOnu5wTJ05w+vRp1q5dC7i+hwMHDpxV7/j4eK/OPykpiXXr1p0Vq7y8nISEhHp/13O9P336dJYv\nX85bb71Feno64eHhXtXnfNMSHiK1qgQaFRXFI488wrx583j33XcpLS2lqqqKdevWcd999wGu7kcX\nXHAB7du354cffuBvf/tbo+V27dr1rL6bt956K3FxcUyYMIGdO3fidDopLy8/q7XXGJvNxsSJE1m8\neDGlpaVkZ2fzxhtv1Lv/mDFjuOqqq5gwYQJfffUVDoeD06dP89JLL/Haa6+RlJTE8OHDeeCBBygv\nL+ebb77h1VdfbVJ3ouXLl5OdnU1paSmLFi0iPT0dm83GhRdeSHl5Oe+99x5VVVU8+uijVFRUuI/r\n2rUrubm5VFdXA66EePXVV/P73/+eU6dOUV1dzb59+/jkk0/OGffmm2/m8ccf5/jx4xQUFLB06VL3\nZ5dddhmRkZE8+eSTlJWV4XQ62blzJ9u2bQNgypQpPProoxw7dozCwkIeeeQRr7+DO+64gwcffNCd\nkI8dO+buzRETE0NISEi9fXprmzZtGu+88w7Lly/n1ltv9aou5yNNoEHo97//Pc888wyPPvooMTEx\nJCUlsXTpUm644QYA/vKXv7BixQoiIyO5/fbbmTRpUqNlLl68mOnTp9OhQwfefvttwsPD+fjjj0lO\nTubXv/41F1xwARdddBHbtm3j7bff9riuS5cupbi4mNjYWG677TZmzJjR4P7/+Mc/GDduHJMmTSIq\nKoqLL76YrKwsxowZA8DKlSvJzc0lPj6eCRMmsGTJEvdn3vjtb3/LbbfdRmxsLOXl5bzwwguA6z+q\n//zP/2T27NkkJCQQERFBYmKi+7ibbroJcF0up6SkAPDmm29SWVlJcnIyHTt2JD09/azbILUtWrSI\nxMREevbsyZgxY0hPT6dNmzaA6z+eNWvW8PXXX9OzZ0+io6OZPXs2J0+eBOChhx4iNTWVAQMGcMkl\nl5CSksJDDz3k1fnPnz+f8ePHc/XVVxMZGcnQoUPd/XzbtWvHgw8+yOWXX06HDh3IzMyst5ykpCRS\nUlIwxrhvNShXAm3r4RYopu7laSN0LLwCYNSoUUybNu1n93QD4W9/+xsZGRn1tlhbgpkzZxIfH8+j\njz4a6Kr4UpPGwl9kjPw/D/e9Ar4SkdSmxPNGq2uBqpbv8OHDbN68merqanbt2sXTTz/NhAkTAl0t\nr+Xm5vK///u/zJo1K9BVCSq+voQ3xow1xuwyxuw1xiw8x+e3GWOOGWO+PrM12jrQBKpanMrKSv7t\n3/6NyMhIRo8ezfXXX8+dd94Z6Gp55eGHH+biiy/m3nvvpWfPnoGuTlDx5VBOY4wNeBG4FkgGphhj\nks+x63+LyMAz298bLVcv4ZVSftKkS/hkY2S5h/sObuQS3hgzDFgsItecef0AgIg8Xmuf24BUEbnL\n0zpqC1QpFZRCsPQQKdoYk1Vrm1OnuAQgr9br/DPv1XWjMeYbY8w/jDENd/gm+PupKqVaKYsd6Qt9\n8BDp/4CVIlJhjPk34A1gdEMHaAtUKRWUfPwQqQCo3aJMPPOem4gUiUhNh+W/A2cPQTwHTaBKqaDk\n4wS6DehjjOlpjAkDJgOrz4pnTFytl+OB7xsrVC/hlVJBy1cJSkQcxpi7gPcBG/CaiHxnjHkE10Qk\nq4G7jTHjAQfwE3BbY+XqU3illL806Sn8QGPkIw8zaGdHYDrSawtUKRWUQkKgbRsPdw7Q5P6aQJVS\nQckYqGfWyaChD5GUT2zbto0BAwZQXl5OSUkJ/fv3Z+fOnYGulmrBDBBq92wLWB31HqjylYceeojy\n8nLKyspITEzkgQceCHSVVGA16R5oaqiRrE4eBvoxMPdANYEqn6msrGTIkCGEh4fzxRdfuGd2V61W\n0xJomJGsGA8DHdKHSKqFKyoqori4mKqqKsrLy4mIiAh0lVRL1gLW9NAWqPKZ8ePHM3nyZHJycjh8\n+PBZM8WrVqlpLdBwI1ndPAy0R1ugqgV78803CQ0N5ZZbbsHpdDJ8+HA++ugjRo9ucCixUvXTFqhS\nqhVrWgu0nZGs3h4G+lZboEopdbYgfw6pCVQpFZxawCV8kFdPKdVqGcDToZwBoglUKRWctAWqlFJe\n0gSqlFJe0gSqlFJNEORP4XU2piZYv349F110Eb179+aJJ57wadl5eXlcccUVJCcn079/f55//nmf\nll+b0+lk0KBB/OY3v/FL+SdOnCA9PZ2+ffvSr18/tmzZ4vMYzz77LP379+fiiy9mypQplJeXN7nM\nmTNn0qVLFy6++GL3ez/99BNXXXUVffr04aqrruL48eNNjqPq4cuF4f1EE6iXnE4n8+bNY926dWRn\nZ7Ny5Uqys7N9Vr7dbufpp58mOzubzMxMXnzxRZ+WX9vzzz9Pv379/FI2wPz58xk7diw//PAD//zn\nP30eq6CggBdeeIGsrCx27tyJ0+kkIyOjyeXedtttrF+//qz3nnjiCa688kr27NnDlVde6fP/OFUt\nIbiewnuyBYgm0DpEBE9GZ23dupXevXvTq1cvwsLCmDx5MqtWrfJZPeLi4khJSQEgMjKSfv36UVBQ\n0MhR1uXn5/Pee+8xe/Zsn5cNcPLkST799FNmzZoFQFhYGB06dPB5HIfDQVlZGQ6Hg9LSUuLj45tc\n5i9/+Us6dTp7PrVVq1Yxffp0AKZPn867777b5DiqHtoCbXkqKyvZt28f1dXVDe5XUFBAUtK/VklN\nTEz0S4IDyM3NZceOHaSlpfm87HvuuYennnqKkBD//FXIyckhJiaGGTNmMGjQIGbPnk1JSYlPYyQk\nJPCHP/yBbt26ERcXR1RUFFdffbVPY9Q4evQocXGuxRtjY2M5evSoX+KoMzSBtiwiQl5eHhUVFTid\nzkBXh+LiYm688Uaee+45LrjgAp+WvWbNGrp06cLgwY0uf+01h8PB9u3bmTt3Ljt27CAiIsLnl73H\njx9n1apV5OTkcOjQIUpKSli+fLlPY5yLMQZjmjTcWzXE4HqI5MkWIJpA62GMYf/+/TgcjnNe0ick\nJJCXl+d+nZ+fT0JCgk/rUFVVxY033sjUqVOZOHGiT8sG2Lx5M6tXr6ZHjx5MnjyZjz76iGnTpvk0\nRmJiIomJie7Wc3p6Otu3b/dpjA8//JCePXsSExNDaGgoEydO5IsvvvBpjBpdu3bl8OHDABw+fJgu\nXbr4JY5CL+FbMmMM+fn55OTkUFVV9bMkOmTIEPbs2UNOTg6VlZVkZGQwfvx4n8UXEWbNmkW/fv1Y\nsGCBz8qt7fHHHyc/P5/c3FwyMjIYPXq0z1tusbGxJCUlsWvXLgA2btxIcnKyT2N069aNzMxMSktL\nERE2btzot4di48eP54033gDgjTfe4Prrr/dLHIUm0PNBfn4+TqeTffv2nZVE7XY7S5cu5ZprrqFf\nv37cfPPN9O/f32dxN2/ezFtvvcVHH33EwIEDGThwIGvXrvVZ+c3pr3/9K1OnTmXAgAF8/fXX/PGP\nf/Rp+WlpaaSnp5OSksIll1xCdXU1c+bMaXK5U6ZMYdiwYezatYvExEReffVVFi5cyIYNG+jTpw8f\nfvghCxcu9MEZqHOqGQsfxE/htSO9B4wx5OXlISL84he/cD9weeGFF9i9e7dfYo4YMQIRYezYsT/r\nSuNrNTFGjRrll/IHDhxIdHS0X89jyZIlLFmyhLFjx/LWW2/5pMyVK1ee8/3Q0FD27NnjkxiqAToS\n6fxQ86AgPz8fgHnz5lFYWEh+fr67q5G/aAzPpaWl8emnn/o1TlNjHDx4kMLCQh/X6jylCfT8k5+f\nz5o1a3A4HIwaNYpNmzb5NZ7G8FxmZiZ79+71aX9cX8cYMWKEj2t0ngvyoZyaQJugOUahaAxr/Jk8\nmzOGQlug57vf/OZ6ysqKLR5lA6z0L7W6f7DG8OaY8yNG+/ZRHD16yGIMRQgQHuhKNEwTaBO4kudi\ni0ctBp60sP/9wAsWY9wNvGJh/9uBZRZjzACsdnmaZjHODKydB7jOxcr3dTfWfg9w/SaLPd67uNjz\nfVUdegmvlFJeaAGX8NoPVCkVnHzckd4YM9YYs8sYs9cYU28HXmPMjcYYMcY0ukyyJtA6KioqGp1I\nRCnVTHw0Ft4YYwNeBK4FkoEpxpifDYkzxkQC84EvPameJtA6ysvLKS0t5eDBg4GuilKtm29boJcB\ne0Vkv4hUAhnAucbh/n+4bop7NCO3JtA6oqKiiIiIoLS0lJKSEm2NKhUovp1QOQHIq/U6/8x7bsaY\nFCBJRN7ztIpBfos2MIwx9O3bl2PHjlFWVsbevXsDXSWlWh9rD5GijTFZtV6/LCIvexzKmBDgGeA2\njyOiCbRBNpuNiIgIbDYbxcXFtG3bFpstyPtVKHU+8TxDFYpIQw99CoCkWq8Tz7xXIxK4GNh0Zuh2\nLLDaGDNeRGonZi+r14r17NmTgoICysrKCAkJYf/+/XppryzJzc3126z/5y3fdmPaBvQxxvTElTgn\nA7fUfCgiJ4Fod2hjNgF/aCh54tPqnedCQkKIiIjA4XDQtm3bM7PVh2C9I30Iro7YVva/24sYt1vc\nf4bFGDZcHeOtsBrH6nnUHGPl+7L6e9Qcs9jS/uHh4cyYMYMffviB1NRUv89OdV6omZHeB0TEYYy5\nC3j/TKmvich3xphHgCwRWe1NuZpALbLb7cTFxeFwOIBqvBvFYmUEzzTgY4sxrgCsTLN3IXDSYowo\noNLiMWEW40Rh7TzAdS5Wvq8r8G5ElbXRZLGxsaxbt44RI0aQlXXuRs3MmTPdy6zs3LkTcC2jPGnS\nJHJzc+nRowdvv/02HTt2tFjfFsrHHelFZC2wts57i+rZd5QnZeo1hVJBQpdRrqMFTKisCVSpIKHL\nKNfRApb00Et4pYJYq15GuQWMhQ/y6imlarTKZZSDvNegXsIrFcRa9TLKLeASXhOoUkGsVS+jXDOh\nsidbgGgCVSpI6DLK5+Cj2Zj8Re+BKhUk6ltGeePGjc1ckyChD5HOdza8G8ViZQSPDVdnbytsuDqU\ne8qOq9O6FXZcHeOtHmMljtXzqDnGyvfl7YgqK797kD8JCVaaQM93Trxbr8jqSBkvRgl1FM93P25g\nmIX9AbYYuNbiMessxtlirJ0HuM7F8mgnb0Z6WV13SXklyP/v0QSqlApO2gJVSikv6bLGSinlPdFL\neKWUsk4MOIM8QwV59ZRSrZYm0JanqKiI0tJSjhw5goi0vrHHSgUJMeCweTrWJzArRGgCraNz5860\nadOGkydPUlJSgs1mo6ioKNDVUqrVEWNw2j1NUVYn9/YNTaDnYLPZuOiiiygqKsLpdHLkyBGKi4ux\n2+3Y7XZKSkrOzEivlGdKSkr0asYiwVBp83SwhibQoGSz2ejfvz8nT57E4XBQVVXFnj17ziwqZ8N6\nJ2mrI2W8HCV03Mo/Vrur07oVxu7qGG/1GEtxrJ7HmWMsj3ayOtLL6rpLNvbt28fvfvc7XRPJAsHg\nCPKe9JpALahpgQ4cOPBMC9QJvGKxlNuxvF6RN6Nxplg4ZqWBNyzGmG4g0+IxQy3GmW7xPMB1LlZH\nYXm17pKV3/12BgwYwMaNGxtcE6muZ599lr///e8YY7jkkktYtmwZ4eFB3jHSx5xBnqJ0NialglBB\nQQEvvPACWVlZ7Ny5E6fTSUZGRqCr1awEgxObR1ugBHd6V6oVczgclJWVERoaSmlpKfHx8YGuUrOq\nSaDBTFugSgWhhIQE/vCHP9CtWzfi4uKIiori6quvDnS1mpVgqCDMoy1QNIEqFYSOHz/OqlWryMnJ\n4dChQ5SUlLB8udX161s2VwvU7tEWKJpAlQpCH374IT179iQmJobQ0FAmTpzIF198EehqNbtgvweq\nCVSpINStWzcyMzMpLS1FRNi4cSP9+vULdLWalT5EUkp5JS0tjfT0dFJSUrDb7QwaNIg5c+YEulrN\nSkD7gSqlvLNkyRKWLFkS6GoEkAn6fqDBXbugZ8PVMd7qMRbXK7I6GsfYXR3KPRVid3Vat8Jmd3WM\nt8JqHKvnAVj/vrxZdykEa797cLeigpVgqAzgE3ZPaAJtEiewzOIxM7C8Zo836xVZHPEzULZYCvG1\nGcbL8ltLx8wxb1mK87UZ5t0IKavrLnmz5pSl332GxfIVtIx+oJpAlVJBScfCK6VUEwT7PVDtxqSU\nCkq+7sZkjBlrjNlljNlrjFl4js/vMMZ8a4z52hjzuTEmubEygzu9K6VarZqhnL5gjLEBLwJXAfnA\nNmPMahHJrrXbChF56cz+44FngLENlasJVCkVlMS33ZguA/aKyH4AY0wGcD3gTqAicqrW/hG4uqI2\nSBOoUiooWXwKH22MqT3R6ssi8nKt1wlAXq3X+UBa3UKMMfOABUAYMLqxoJpAlVJBy0ICLRSR1KbG\nE5EXgReNMbcADwHTG9pfE2gdZWVlVFVVUVhYiNPpxBhDVVVVoKulVKvj425MBUBSrdeJZ96rTwbw\nt8YK1QRah4hQXV1NUVERlZWViAg7duyguLjYvc/mzZsRsdjBW7VqmZmZhIaGBroaLYqP74FuA/oY\nY3riSpyTgVtq72CM6SMie868/DWwh0ZoAq2jXbt2tGnTxr0qJ8Bll1121lRil19++Zk1kWxYH2Vi\nddEzLxZ8szpk0m5zjfqxFMIwx7xlrV5W49i8GGLqzcJ1lhftC8Ha725j6NChXH/99ZYWlTtx4gSz\nZ89m586dGGN47bXXGDbM2u/UkvlyKKeIOIwxdwHv4/qH+5qIfGeMeQTIEpHVwF3GmDFAFXCcRi7f\nQRNoEzkBq5PcTsPaEqxhcK3F1u46iwu+DTVeDctcbK1WLHY4LcWZY97ybuE6K9/XOoP1JXHDsPa7\nTwNg1apVlhaVmz9/PmPHjuUf//gHlZWVlJaWWqxny+broZwishZYW+e9RbX+PN9qmdqRXqkgdPLk\nST799FNmzZoFQFhYGB06dGj0uEWLFvHcc8+5Xz/44IM8//zzfqunvzmwebQFiiZQpYJQTk4OMTEx\nzJgxg0GDBjF79mxKSkoaPW7mzJm8+eabAFRXV5ORkcG0adP8XV2/0CU9lFJecTgcbN++nblz57Jj\nxw4iIiJ44oknGj2uR48edO7cmR07dvDBBx8waNAgOnfu3Aw19j2dkV4p5ZXExEQSExNJS3P19U5P\nT/cogQLMnj2b119/nSNHjjBz5kx/VtPvgn06O22BKhWEYmNjSUpKYteuXQBs3LiR5ORG57YAYMKE\nCaxfv55t27ZxzTXX+LOaflVNCBW08WgLFG2BKhWk/vrXvzJ16lQqKyvp1asXy5Z5NolzWFgYV1xx\nBR06dMBmC+4WXGOCvQWqCVSpIDVw4ECPuzzVVl1dTWZmJv/zP//jh1o1n5YwI71ewit1HsnOzqZ3\n795ceeWV9OnTJ9DVaTJ9iHRes1HTSdpzdrAyusLYz3T2tsDigm/ejCoKAcsd6S3H8WbhOsvfl8Xf\nA7D+uzffP/Dk5GT279/fbPH8SZf0OO81w6Jy4v9F5ap1UTlrMXRRuWbhGsoZuAdEntAEqpQKSi3h\nHqgmUKVUUNJLeKWUaoJgX5UzuGunlGq19BJeKaW8pAlUKaW85Mtljf1FE6hSKij5eEkPvwju2gWR\n6upqnE4n1dXV7Nq1i+rq6kBXSbUge/bswW7Xf25W6SV8CyQi/PTTT1RUVOB0Otm8eTNlZWXY7XZC\nQkLo1KkTTqcTXRNJ10TyjI2OHTty6623WloTqbXTe6AtUFFREaWlpRw5coSQkBBCQ0MZPnw4W7b8\nawRNTEzMmUXlnMArFiPcDuy2sP+F0NHiaJzjBqZYOGaltZFL4Bq95NV6RVbiTLd4HuA6Fyvf13GD\ntd8D4EKs/e63Ex0dzdq1ay2tiQTgdDpJTU0lISGBNWvWWKxny9YS+oHqZCJ1dO7cmYiICJKTkwkN\nDSUkJARjLLaClPKR559/nn79+gW6GgGjS3oopbySn5/Pe++9x+zZswNdlYCoJoRKwjzaAkUv4ZUK\nUvfccw9PPfUUp0+fDnRVAkYv4ZVSlq1Zs4YuXbowePDgQFclYFrCqpzaAlUqCG3evJnVq1ezdu1a\nysvLOXXqFNOmTWP58uWBrlqr+YyCAAAPs0lEQVSzaQlP4bUFqlQQevzxx8nPzyc3N5eMjAxGjx7d\nqpJnDZ2RXimlvFCtQzmVUk01atQoRo0aFehqBIAO5TzP2XB1jLd6zIUW9ref6extgbG7OpR7yurI\nJfBuvSKrcayeB2D9+7L6e4DrzpeV3z247+MFq5ZwD1QTaJM4gRcsHnM38LGF/a/A8po9EmV9NI43\n6y5da/GYdV6sV+TNKCxL31cU1n4PcP0mVn73uy2Wr2poAlVKKS/oUE6llPKSr/uBGmPGGmN2GWP2\nGmMWnuPzBcaYbGPMN8aYjcaY7o2VqS1QpVRQci1r7Jun8MYYG/AicBWQD2wzxqwWkexau+0AUkWk\n1BgzF3gKmNRQudoCVUoFJcHgrLZ5tHngMmCviOwXkUogA7j+rHgiH4tI6ZmXmUBiY4VqC1QpFZwE\nHA6P74FGG2NqzxP4soi8XOt1ApBX63U+kNZAebOAdY0F1QSqlApKIganw+MUVSgiqb6Ia4yZBqQC\nv2psX02gSqmg5EqgPnsKXwAk1XqdeOa9sxhjxgAPAr8SkYrGCtUEapHT6eTEiRNnlvRQyjMnT57U\nibmtEnyZQLcBfYwxPXElzsnALbV3MMYMAv4fMFZEfvSkUE2gHnI4HFRUVGCMoaCg4Myicjasd5K2\n4eqI7Slv1uyxOhrHi3WXjN3VMd7qMVbXK7I6Csvy92X19wDXs1crv7uNQ4cOcffdd+uaSBaIhFBZ\n3sZHZYnDGHMX8D6uH/01EfnOGPMIkCUiq4H/ANoD/3PmP7uDIjK+oXI1gTbC4XCwdetWKisrCQ8P\nx2az0b9//1prIj1pscT7ASuz6kzDu5EyFtdd8ma0E5UWjwmzGCcK79YrsjrSy+osR9Ow9rvfT79+\n/diwYYPHayLl5eVx6623cvToUYwxzJkzh/nz51usZwsngO9aoIjIWmBtnfcW1frzGKtlagKtR1FR\nESUlJYSEhJCSksI333wT6CqpVsRut/P000+TkpLC6dOnGTx4MFdddRXJycmBrlrzEePTBOoPmkDr\nOH36NCUlJeTn59O2bVtCQkJo3759oKulWpm4uDji4uIAiIyMpF+/fhQUFLSyBAo4gvu+sXakryM0\nNJS2bdty6aWXEhKiX48KvNzcXHbs2EFaWkPdFs9TDg+3ANEWaB3h4eGaOFXQKC4u5sYbb+S5557j\nggsuCHR1mlc1UB7oSjRME6hSQaqqqoobb7yRqVOnMnHixEBXp/kJUBXoSjRME6hSQUhEmDVrFv36\n9WPBggWBrk5gCK6OLkFMr1WVCkKbN2/mrbfe4qOPPmLgwIEMHDiQtWvXNn7g+UbvgSqlrBoxYgQi\nFmfjP98IAU2OntAE2iQ2XB3jrQjB1RHbSgyrI2W8WHfJm9FOludq9GaUkNX1iqx+Xzas/R7g+g2t\n/O7B3ZcxaGkCPd85gcUWj1mM1VEs3q279IqF/W8HllmMMQPvRvBYiTMDa+cBrnOxul6RN6PJFlvY\n38q+yk2fwiulVBNoC1Qppbyg3ZiUUspLLaAbkyZQpVRw0odISinlJX2IpJRSTaAtUKWU8oJewiul\nlJdaQALVsfAWOJ1OiouL2bx5M5mZmYGujmpBMjMzueKKK9xrIo0dOzbQVQp+Nd2YPNkCxFgcb3ve\nD84tLy9ny5YtDB8+nC+++AKAYcOG8cknn1BVVUXbtm0ZOXIkDoeD6OiulJUVW4xgw1rfDKv7B2sM\nb445P2K0bx/F0aOHANcY9+3bt3t03Pr165k/fz5Op5PZs2ezcOFCi/UMuCZNJ28SUoV5ja8fBcCD\n5itfrQtvhV7CN0JE2LlzJ06nk3bt2gGuJFtRUcH//d+7DB482G+xq6ur2b59O6mp/vt7ISJs377d\nr+cB8NVXX/k9RlZWFoMHD/br8sFZWVkMGjQIm83a+PbKykrWrl3L6dOnPdrf6XQyb948NmzYQGJi\nIkOGDGH8+PGtb0kPfQrfclVXV1NWVka3bt3cf/GNMXz55ZeUl5cTFhbGV1995bf4Ncso+zNGdXU1\nFRUVfo0BUFpaSlZWll+TW2VlJVu3bsVu999fa4fDwZYtWwgPD7d8Ls888wzHjh2jW7duJCcnN7is\n8datW+nduze9evUCYPLkyaxatar1JVC9B9oyHTt2jNLSUsLDw0lMTEREMMZQWVlJeXk54eHhhIaG\nYozxy+Z0OhER2rRp47cYxhgcDodfz6M5tzZt2lBZ6Vpq2V8xwsLCsNvtVFRUWI7z1FNP0adPH6qq\nqtwt8vruhRYUFJCUlOR+nZiYSEFBgf//4geTFnAPVBNoHSJCRUUFBw4cICIiApvNhtPpxGazUVFR\nQWVlJW3btrV8CWdFTaswPDzcbzFqOBwOv7bYahhjqK6u9nsMu91OVZV//0WFhYVhs9koLy+3PGfn\nk08+yfLly4mPjycvL4/Dhw/rA6X61Azl9GQLEE2gdRw7dgwRcd9LCwkJ4csvv6S0tBSHw+Fe6thf\nRMTdwjXGv0u6VldXu1tH/hYSEtIsEwSHhYVRVVXl91hhYWGEhIRQXm79Jp0xhmeffdbdqjxw4MDP\nnswnJCSQl5fnfp2fn09CQoJP6t6i6Iz0LUuXLl3Yt28f4Epml156KdnZ2XTq1IlevXr5Pdns3r2b\nuLi4sy7f/OXAgQOEhoYSHx/v91g1l5/NkQTy8vJwOp306NHD77H2799PRUUFffv2tfx345NPPmHv\n3r3MmjWL+fPnM23avyZ2HjJkCHv27CEnJ4eEhAQyMjJYsWKFr6sf3FrAPVBNoHWIiPsyHuCzzz4j\nLCyMsrIyioqK/Brb4XDgcDgIDw/n8OHDfo0Frgc7bdu2JT8/3++xHA4H1dXVzXYfr7S0lKNHjzZL\n67qiooLPP/+cNm3aeHW8zWbj3nvv5d577+XSSy/l/fffx263s3TpUq655hqcTiczZ86kf//+Pq55\nkGsBY+G1H2gdFRUVZGZmuh/iVFdX+/V+Z23NeUkNuO/tNoea/5j8efujtpb2XS5cuJDCwkLCw8Np\n164d0dHRDT6lbyGa1g+0c6rwaw/7gb6l/UCDQps2bfjVr34V6GqoVmbr1q2BrkJw0kt4pZTygs5I\nr5RSXtIZ6ZVSykst4CGS9gNVKkisX7+eiy66iN69e/PEE0/87POKigomTZpE7969SUtLIzc3t/kr\n2Zx8PBLJGDPWGLPLGLPXGPOzmVmMMb80xmw3xjiMMemelKkJVKkgUDN5yLp168jOzmblypVkZ2ef\ntc+rr75Kx44d2bt3L7/73e+4//77A1TbZuSjkUjGGBvwInAtkAxMMcbUnVjgIHAb4HGHW72EVyoI\n1Ewesnv3bq699loKCwtZsGDBWV2ZVq1axUUXXURycjI2m40ffviB3NzcZhkwEBC+7Uh/GbBXRPYD\nGGMygOsB9/9SIpJ75jOPxxxrC1SpIFBQUEBCQoK7FTp9+nQ2bNhAt27d3JfzBQUFjBgxgqysLL79\n9ls6dOjAzTffjDGGrCwP+0u2JDUJ1LOhnNHGmKxa25w6pSUAebVe5595r0m0BapUkDh27Bi9e/em\ne/fu/Nd//RcDBgxg4sSJrFy5kvHjxwMwfPhw97y0oaGhfP/996SlpQWy2v5jrRtTYSA60msLVKkg\nkJCQwMGDB0lKSmLr1q1ERUXRp08ftm7dyqFDhxg5ciSVlZXuCUYcDgc//vgj119/PadOneLmm2+m\nf//+3HLLLQE+Ex8SoMLDrXEFQO0JJhLPvNckmkCVCgJDhgzhyJEjnD59mgMHDlBYWMill17Kp59+\nysKFCxk6dCg5OTlcffXVPPHEE9xyyy2EhITwwAMPkJeXx5///Ge6dOnCt99+y4ABA1i7dm2gT6np\nrF3CN2Yb0McY09MYEwZMBlY3tYp6Ca9UELDb7dx3330sWrSITZs20atXL/Lz87HZbBw8eJDPP/+c\nu+66iw8++ICHH34Yh8PBO++8wxtvvEF8fDxvv/02N998M3PnziU7O5tx48a1/G5OPhyJJCIOY8xd\nwPu4FrV6TUS+M8Y8AmSJyGpjzBDgHaAjcJ0xZomINDiDi04molSQcDgcXHjhhfzHf/wHL730Ert3\n7yY1NZUuXbqwceNGYmNj2bp1K1VVVYSFhdG1a1d+/PFHKisrERGio6MZOnQoX331FcePH+ezzz4j\nJSUlkKfUtMlE2qQKCR4+HMsJzGQiegmvVJComcJu4cKFbNq0iQEDBhAVFcWKFSuIjo5m5MiRREVF\nARAREUGHDh2IjIykQ4cOrFq1CrvdzurVqzl9+jQvvvgic+fODfAZNZFvL+H9QhOoUkFk3Lhx7Nmz\nh1WrVvH111+TkZHBuHHjSE5OZsuWLVx++eXExcUxefJkvv76ayZMmEB0dDQbN250L1b3zDPP8NRT\nT3HixIlmmVfWrzSBKqWsGjduHDk5OcTGxpKens6BAwcoKirijjvuoKqqyj2z/w033EBaWhoffPAB\noaGhHDt2jBtuuIHy8nK6dOnSsheiqxkL78kWIJpAlQpSdS/px4wZQ48ePSgqKiIyMhKAa665hs6d\nO3PgwAG2bt3KnXfeyY8//uhedrtFawGX8PoQSakWYO3atdxzzz2Ul5dTUVHB0aNHWbRoEampqYwf\nP57s7GxGjx5NWFgYnTp14qmnnuLf//3f2bRpE3FxcYGqdtMeIoWkCuEePkQq04dISql6jBs3jt27\nd/Ppp58SExMDwCOPPOIeoZScnMyrr75K//792bFjBxdccAFRUVFnJc+XXnqJgQMHMnDgQHr27MkV\nV1wRkHPxWAtYF15boEq1EFOmTGHTpk0UFhbStWtXlixZQlWVK3vccccdiAh33XUX69evp127dixb\ntozU1J83yqqqqhg9ejT33Xcf1113nT+r3LQWqEkVjIctUAlMC1QTqFKtzJ133klMTAxLlizxd6im\nJ1A8nSRFF5VTSvnZ66+/zoEDB1i6dGmgq3Je0ASqVCvx1Vdf8Ze//IXPPvus2ZaXPt9pAlWqlVi6\ndCk//fST++FRamoqf//73wNcq4YE/7Kceg9UKeUvTbwHmiKw2cO92+k9UKWU+pfgb4FqAlVKBalq\noCzQlWiQJlClVJDSFqhSSjVBAAe6e0ATqFIqSGkLVCmlvOTbheH9QROoUipIaQtUKaW8pE/hlVLK\nS3oJr5RSXtJLeKWU8pK2QJVSykvaAlVKKS8J+hBJKaW8oi1QpZTykt4DVUopL2kLVCmlvKQtUKWU\n8pK2QJVSyks6lFMppbykl/BKKeWl4L+Et7oqp1JKNQtjzHog2sPdC0VkrD/rcy6aQJVSykshga6A\nUkq1VJpAlVLKS5pAlVLKS5pAlVLKS5pAlVLKS5pAlVLKS5pAlVLKS5pAlVLKS5pAlVLKS/8/Xw8L\nmet0CZkAAAAASUVORK5CYII=\n",
      "text/plain": [
       "<matplotlib.figure.Figure at 0x7fb526161780>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "problem = elliptic.Elliptic(g, d)\n",
    "p = problem.solve()\n",
    "plot_grid(g, p)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Add fractures\n",
    "We now try to solve the same problem, but with a fracture in the domain. We create a multidimensional grid:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "f = np.array([[0,10],[5,5]])\n",
    "gb = meshing.cart_grid([f], [10,10])\n",
    "gb.assign_node_ordering()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We now make use of the DarcyData class to assign data to the fracture and matrix. We wish to set zero dirichlet boundary conditions. However, the data class assigns Neumann conditions by default, so we overload the bc function. We set a small aperture for the fracture, but a high permeability. Note that we let the FractureDomain innherit from the MatrixDomain. This way we assign the same parameters to the fractures as the matrix, unless we overload the parameter function(e.g., the permeabillity) "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "class MatrixDomain(elliptic.EllipticData):\n",
    "    def __init__(self, g, d):\n",
    "        elliptic.EllipticData.__init__(self, g, d)\n",
    "\n",
    "    def bc(self):\n",
    "        dir_bound = np.ravel(np.argwhere((self.grid().has_face_tag(FaceTag.DOMAIN_BOUNDARY))))\n",
    "        return bc.BoundaryCondition(self.grid(), dir_bound, ['dir']*dir_bound.size)\n",
    "\n",
    "class FractureDomain(MatrixDomain):\n",
    "    def __init(self, g, d):\n",
    "        MatrixDomain.__init__(self, g, d)\n",
    "        \n",
    "    def permeability(self):\n",
    "        kxx = 100 * np.ones(self.grid().num_cells)\n",
    "        return tensor.SecondOrder(2, kxx)\n",
    "    \n",
    "    def source(self):\n",
    "        val = np.ones(self.grid().num_cells)\n",
    "        val[round(self.grid().num_cells/2)] = 1\n",
    "        return val\n",
    "    \n",
    "    def aperture(self):\n",
    "        val = 0.01 * np.ones(self.grid().num_cells)\n",
    "        return val\n",
    "    \n",
    "def assign_darcy_data(gb):\n",
    "    gb.add_node_props(['problem'])\n",
    "    for g, d in gb:\n",
    "        if g.dim == 2:\n",
    "            d['problem'] = MatrixDomain(g, d)\n",
    "        else:\n",
    "            d['problem'] = FractureDomain(g, d)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We are now ready to declare the problem and solve it"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<matplotlib.figure.Figure at 0x7fb5261412e8>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "assign_darcy_data(gb)\n",
    "problem = elliptic.Elliptic(gb)\n",
    "problem.solve()\n",
    "problem.split('pressure')\n",
    "plot_grid(gb, 'pressure')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Change discretization\n",
    "By default, the darcy solver uses the TPFA discretization for the fluxes. If we set a anisotropic permeability tensor tpfa will not give a consistent discretization. In these cases we would like to use, e.g., the MPSA discretization. We can do this by overloading the flux_disc() function of the darcy solver. Note that we have already assigned data to the grid, so we do not have to do this again"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from porepy.numerics.fv import mpfa\n",
    "class DarcyMPFA(elliptic.Elliptic):\n",
    "    def __init__(self, gb):\n",
    "        elliptic.Elliptic.__init__(self, gb)\n",
    "    \n",
    "    def flux_disc(self):\n",
    "        return mpfa.MpfaMixDim()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "problem = DarcyMPFA(gb)\n",
    "problem.solve()\n",
    "problem.split('pressure')\n",
    "plot_grid(gb, 'pressure')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
