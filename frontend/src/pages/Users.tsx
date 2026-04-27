import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getUsers, updateUser, deleteUser } from '@/api/users'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { useToast } from '@/components/ui/toast'
import { Checkbox } from '@/components/ui/checkbox'
import { Label } from '@/components/ui/label'
import { Search, Trash2, Lock, Power, PowerOff, Shield, User } from 'lucide-react'
import type { User as UserType } from '@/api/users'

export default function UsersPage() {
  const queryClient = useQueryClient()
  const { addToast } = useToast()
  const [searchName, setSearchName] = useState('')
  const [editingUser, setEditingUser] = useState<UserType | null>(null)
  const [isEditOpen, setIsEditOpen] = useState(false)
  const [isResetOpen, setIsResetOpen] = useState(false)
  const [newPassword, setNewPassword] = useState('')

  const { data: users, isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: getUsers,
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Parameters<typeof updateUser>[1] }) => updateUser(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
      setIsEditOpen(false)
      addToast({ title: '成功', description: '用户信息已更新' })
    },
    onError: () => addToast({ title: '错误', description: '更新失败', variant: 'destructive' }),
  })

  const deleteMutation = useMutation({
    mutationFn: deleteUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
      addToast({ title: '成功', description: '用户已删除' })
    },
    onError: (err: { response?: { data?: { detail?: string } } }) => {
      addToast({ title: '错误', description: err.response?.data?.detail || '删除失败', variant: 'destructive' })
    },
  })

  const filteredUsers = users?.filter((u) =>
    !searchName || u.username.includes(searchName)
  )

  const handleToggleActive = (u: UserType) => {
    if (u.username === 'admin') {
      addToast({ title: '提示', description: '不能禁用默认管理员账号', variant: 'destructive' })
      return
    }
    updateMutation.mutate({ id: u.id, data: { is_active: u.is_active ? 0 : 1 } })
  }

  const handleSaveEdit = () => {
    if (!editingUser) return
    const roles: string[] = []
    if (editingUser.roles.includes('admin')) roles.push('admin')
    if (editingUser.roles.includes('teacher')) roles.push('teacher')
    updateMutation.mutate({
      id: editingUser.id,
      data: { roles: roles.join(',') },
    })
  }

  const handleResetPassword = () => {
    if (!editingUser || !newPassword.trim()) return
    updateMutation.mutate({
      id: editingUser.id,
      data: { password: newPassword.trim() },
    })
    setIsResetOpen(false)
    setNewPassword('')
  }

  const openEdit = (u: UserType) => {
    setEditingUser({ ...u })
    setIsEditOpen(true)
  }

  const openReset = (u: UserType) => {
    setEditingUser({ ...u })
    setNewPassword('')
    setIsResetOpen(true)
  }

  const toggleRole = (role: string) => {
    if (!editingUser) return
    const roles = editingUser.roles.split(',').filter((r) => r.trim())
    if (roles.includes(role)) {
      setEditingUser({ ...editingUser, roles: roles.filter((r) => r !== role).join(',') })
    } else {
      setEditingUser({ ...editingUser, roles: [...roles, role].join(',') })
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">用户管理</h1>
        <div className="flex items-center gap-2">
          <Search className="h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="搜索用户名"
            value={searchName}
            onChange={(e) => setSearchName(e.target.value)}
            className="w-48"
          />
        </div>
      </div>

      {isLoading ? (
        <div className="text-muted-foreground">加载中...</div>
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>用户名</TableHead>
              <TableHead>角色</TableHead>
              <TableHead>状态</TableHead>
              <TableHead>创建时间</TableHead>
              <TableHead className="text-right">操作</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredUsers?.map((u) => (
              <TableRow key={u.id}>
                <TableCell>{u.id}</TableCell>
                <TableCell className="font-medium">{u.username}</TableCell>
                <TableCell>
                  <div className="flex gap-1">
                    {u.roles.split(',').filter((r) => r.trim()).map((r) => (
                      <span
                        key={r}
                        className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${
                          r === 'admin'
                            ? 'bg-red-100 text-red-700'
                            : 'bg-blue-100 text-blue-700'
                        }`}
                      >
                        {r === 'admin' ? (
                          <Shield className="mr-1 h-3 w-3" />
                        ) : (
                          <User className="mr-1 h-3 w-3" />
                        )}
                        {r === 'admin' ? '管理员' : '教师'}
                      </span>
                    ))}
                  </div>
                </TableCell>
                <TableCell>
                  <span
                    className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${
                      u.is_active
                        ? 'bg-green-100 text-green-700'
                        : 'bg-gray-100 text-gray-700'
                    }`}
                  >
                    {u.is_active ? '启用' : '禁用'}
                  </span>
                </TableCell>
                <TableCell className="text-muted-foreground text-sm">
                  {new Date(u.created_at).toLocaleString()}
                </TableCell>
                <TableCell className="text-right">
                  <div className="flex items-center justify-end gap-1">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => openEdit(u)}
                      title="编辑角色"
                    >
                      <Shield className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => openReset(u)}
                      title="重置密码"
                    >
                      <Lock className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleToggleActive(u)}
                      title={u.is_active ? '禁用' : '启用'}
                    >
                      {u.is_active ? (
                        <PowerOff className="h-4 w-4 text-orange-500" />
                      ) : (
                        <Power className="h-4 w-4 text-green-500" />
                      )}
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => deleteMutation.mutate(u.id)}
                      disabled={u.username === 'admin'}
                      title={u.username === 'admin' ? '不能删除默认管理员' : '删除'}
                    >
                      <Trash2 className="h-4 w-4 text-destructive" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}

      <Dialog open={isEditOpen} onOpenChange={setIsEditOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>编辑用户角色 - {editingUser?.username}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="flex items-center gap-4">
              <label className="flex items-center gap-2 cursor-pointer">
                <Checkbox
                  checked={editingUser?.roles.includes('admin') ?? false}
                  onCheckedChange={() => toggleRole('admin')}
                />
                <span>管理员</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <Checkbox
                  checked={editingUser?.roles.includes('teacher') ?? false}
                  onCheckedChange={() => toggleRole('teacher')}
                />
                <span>教师</span>
              </label>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsEditOpen(false)}>
              取消
            </Button>
            <Button onClick={handleSaveEdit} disabled={updateMutation.isPending}>
              保存
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={isResetOpen} onOpenChange={setIsResetOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>重置密码 - {editingUser?.username}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="newPassword">新密码</Label>
              <Input
                id="newPassword"
                type="password"
                placeholder="请输入新密码"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsResetOpen(false)}>
              取消
            </Button>
            <Button onClick={handleResetPassword} disabled={!newPassword.trim() || updateMutation.isPending}>
              确认重置
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
